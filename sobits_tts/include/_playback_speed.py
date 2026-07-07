# sobits_tts/include/_playback_speed.py
import io
from typing import Tuple

import numpy as np
import soundfile as sf

_SPEED_EPSILON = 1e-6
_MIN_SPEED = 0.5
_MAX_SPEED = 2.0
_MAX_SUPPORTED_CHANNELS = 2


def apply_playback_speed(audio_buffer: io.BytesIO, speed: float) -> Tuple[io.BytesIO, float]:
    """
    Change the playback speed of already-generated audio (PCM16 WAV) while preserving pitch.
    Backend-independent post-processing step, called from execute_callback right after
    generate_audio(), outside the BaseTTSModel contract.

    :param audio_buffer: io.BytesIO containing PCM16 WAV
    :param speed: playback speed multiplier (0.5-2.0). 1.0 is treated as a no-op.
    :return: (io.BytesIO(PCM16 WAV) after conversion, resulting duration in seconds)
    """
    audio_buffer.seek(0)

    # Check the no-op case from header metadata only, without decoding the full buffer.
    # This keeps the default (speed==1.0) path as cheap as before this feature existed,
    # and avoids failing on audio that soundfile can't fully decode but pygame still could.
    if abs(speed - 1.0) < _SPEED_EPSILON:
        duration = sf.info(audio_buffer).duration
        audio_buffer.seek(0)
        return audio_buffer, duration

    if not np.isfinite(speed) or not (_MIN_SPEED <= speed <= _MAX_SPEED):
        raise ValueError(f"playback_speed must be finite and within [{_MIN_SPEED}, {_MAX_SPEED}], got {speed}.")

    data, sample_rate = sf.read(audio_buffer, dtype="float32", always_2d=True)  # (samples, channels)

    num_channels = data.shape[1]
    if num_channels > _MAX_SUPPORTED_CHANNELS:
        raise ValueError(f"playback_speed is not supported for audio with {num_channels} channels (max {_MAX_SUPPORTED_CHANNELS}).")
    layout = "mono" if num_channels == 1 else "stereo"

    stretched = _atempo_filter(data, sample_rate, speed, layout)

    max_abs = float(np.max(np.abs(stretched))) if stretched.size else 0.0
    if max_abs > 1.0:
        stretched = np.clip(stretched, -1.0, 1.0)

    out_buffer = io.BytesIO()
    sf.write(out_buffer, stretched.T, sample_rate, format="WAV", subtype="PCM_16")
    out_buffer.seek(0)

    duration = stretched.shape[1] / sample_rate
    return out_buffer, duration


def _atempo_filter(data: np.ndarray, sample_rate: int, speed: float, layout: str) -> np.ndarray:
    """
    Time-stretch data (samples, channels) in-process via PyAV's (libavfilter) atempo filter.
    Returns a (channels, samples) float32 array.
    """
    # Imported lazily so that 'av' is only a hard dependency when playback_speed != 1.0
    # is actually requested, not for the whole node at import time.
    try:
        import av
        import av.filter
    except ImportError as e:
        raise ImportError(
            "playback_speed != 1.0 requires the 'av' package (PyAV). "
            "Install it with: pip3 install av --break-system-packages"
        ) from e

    planar = np.ascontiguousarray(data.T)  # abuffer requires planar (channels, samples)

    graph = av.filter.Graph()
    abuffer = graph.add_abuffer(sample_rate=sample_rate, format="fltp", layout=layout)
    atempo = graph.add("atempo", str(speed))
    # atempo's output can silently switch from planar (fltp) to packed (flt), which breaks
    # naive to_ndarray() channel separation. Force the output format back to fltp.
    aformat = graph.add("aformat", "sample_fmts=fltp")
    sink = graph.add("abuffersink")
    abuffer.link_to(atempo)
    atempo.link_to(aformat)
    aformat.link_to(sink)
    graph.configure()

    frame = av.AudioFrame.from_ndarray(planar, format="fltp", layout=layout)
    frame.sample_rate = sample_rate

    out_chunks = []
    graph.push(frame)
    graph.push(None)  # flush
    while True:
        try:
            out_chunks.append(graph.pull().to_ndarray())
        except (av.error.EOFError, av.error.BlockingIOError):
            break

    if not out_chunks:
        raise ValueError("atempo filter produced no output frames; input audio may be too short.")

    return np.concatenate(out_chunks, axis=1)