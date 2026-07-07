from rclpy.node import Node

from supertonic import TTS
import soundfile as sf
import io
import gc
import time

from typing import Tuple
from sobits_tts.include._base_tts import BaseTTSModel

class SupertonicTTSModel(BaseTTSModel):
    def __init__(self, node: Node, sample_rate: int):
        super().__init__(node, sample_rate)

        self._node.declare_parameter('supertonic.device', '')
        self._node.declare_parameter('supertonic.intra_op_num_threads', 0)
        self._node.declare_parameter('supertonic.inter_op_num_threads', 0)
        self._node.declare_parameter('supertonic.voice_name', 'F1')
        self._node.declare_parameter('supertonic.total_steps', 5)
        self._node.declare_parameter('supertonic.speed', 1.05)
        self._node.declare_parameter('supertonic.max_chunk_length', 300)
        self._node.declare_parameter('supertonic.silence_duration', 0.3)
        self._node.declare_parameter('supertonic.language', 'en')

        device_param = str(self._node.get_parameter('supertonic.device').get_parameter_value().string_value).lower()
        intra = self._node.get_parameter('supertonic.intra_op_num_threads').get_parameter_value().integer_value
        inter = self._node.get_parameter('supertonic.inter_op_num_threads').get_parameter_value().integer_value

        if device_param not in ('', 'cpu'):
            self._logger.warn(f"[Supertonic] device='{device_param}' is not supported in this build (CPU-only). Falling back to CPU.")
        self._logger.info("[Supertonic] Mode: CPU")

        try:
            try:
                self.supertonic_tts = TTS(
                    model="supertonic-3",
                    auto_download=False,
                    intra_op_num_threads=intra if intra > 0 else None,
                    inter_op_num_threads=inter if inter > 0 else None
                )
            except FileNotFoundError:
                self._logger.warn("[Supertonic] Model not found in local cache. Falling back to auto-download.")
                self.supertonic_tts = TTS(
                    model="supertonic-3",
                    auto_download=True,
                    intra_op_num_threads=intra if intra > 0 else None,
                    inter_op_num_threads=inter if inter > 0 else None
                )
            self._logger.info(f"[Supertonic] Successfully initialized from: {self.supertonic_tts.model_dir}")
        except Exception as e:
            self._logger.error(f"[Supertonic] Initialization failed: {e}")
            raise RuntimeError(f"Supertonic initialization failed: {e}")

    def generate_audio(self, text: str) -> Tuple[float, io.BytesIO]:
        try:
            params = self._node.get_parameters([
                'supertonic.voice_name', 'supertonic.total_steps',
                'supertonic.speed', 'supertonic.max_chunk_length',
                'supertonic.silence_duration', 'supertonic.language'
            ])
            v_name, t_steps, spd, m_chunk, s_dur, lang_code = [p.value for p in params]

            start_time = time.time()
            style = self.supertonic_tts.get_voice_style(voice_name=v_name)
            wav, duration = self.supertonic_tts.synthesize(
                text=text,
                voice_style=style,
                total_steps=t_steps,
                speed=spd,
                max_chunk_length=m_chunk,
                silence_duration=s_dur,
                lang=lang_code,
                verbose=False
            )
            inference_time = time.time() - start_time
            self._logger.info(f"[Supertonic] Inference time: {inference_time:.3f}s for {len(text)} chars (Lang: {lang_code})")

            wav = wav.flatten()
            actual_sr = self.supertonic_tts.sample_rate

            audio_buffer = io.BytesIO()
            sf.write(audio_buffer, wav, actual_sr, format='WAV', subtype='PCM_16')
            audio_buffer.seek(0)

            return float(duration[0]), audio_buffer

        except Exception as e:
            self._logger.error(f"[Supertonic] Generation error: {e}")
            gc.collect()
            return 0.0, None

    def __del__(self):
        if hasattr(self, 'supertonic_tts'):
            del self.supertonic_tts
        gc.collect()
