import io
import os
import time
import numpy as np
import soundfile as sf
import onnxruntime as ort
from pathlib import Path
from typing import Tuple
from piper import PiperVoice
from piper.config import SynthesisConfig
import piper.download_voices as piper_dl

from rclpy.node import Node
from sobits_tts.include._base_tts import BaseTTSModel

class PiperTTSModel(BaseTTSModel):
    def __init__(self, node: Node, sample_rate: int):
        super().__init__(node, sample_rate)
        self._node.declare_parameter('piper.model_path', 'en_US-lessac-medium')
        self._node.declare_parameter('piper.length_scale', 1.0)
        self._node.declare_parameter('piper.noise_scale', 0.667)
        self._node.declare_parameter('piper.noise_w_scale', 0.8)
        self._node.declare_parameter('piper.volume', 1.0)
        self._node.declare_parameter('piper.speaker_id', 0)

        raw_model_path = self._node.get_parameter('piper.model_path').get_parameter_value().string_value

        if '/' not in raw_model_path:
            model_name = raw_model_path.replace('.onnx', '')
            model_path_str = os.path.expanduser(f'~/.sobits_tts/piper/{model_name}.onnx')
        else:
            model_path_str = os.path.expanduser(raw_model_path)

        config_path_str = f"{model_path_str}.json"        
        model_path = Path(model_path_str)
        config_path = Path(config_path_str)

        if not model_path.exists() or not config_path.exists():
            if '/' in raw_model_path:
                raise RuntimeError(f"Piper model not found at {model_path} (Auto-download disabled for full path).")

            model_name = raw_model_path.replace('.onnx', '')
            download_dir = Path(os.path.expanduser("~/.sobits_tts/piper"))
            download_dir.mkdir(parents=True, exist_ok=True)

            self._logger.warn(f"[Piper] Model '{model_name}' not found. Downloading...")
            try:
                piper_dl.download_voice(model_name, download_dir)
                self._logger.info(f"[Piper] Successfully downloaded '{model_name}'.")
            except Exception as e:
                raise RuntimeError(f"Failed to download Piper model '{model_name}'. Error: {e}")

        try:
            self._logger.info(f"[Piper] Loading Model: {model_path.name}")
            self.voice = PiperVoice.load(str(model_path), config_path=str(config_path), use_cuda=False)
            self.actual_sr = self.voice.config.sample_rate
            self._logger.info(f"[Piper] Successfully loaded on CPU. (SR: {self.actual_sr}Hz)")
        except Exception as e:
            self._logger.error(f"[Piper] Failed to load model or config: {e}")
            raise RuntimeError(f"Piper initialization failed: {e}")

    def generate_audio(self, text: str) -> Tuple[float, io.BytesIO]:
        try:
            l_scale = self._node.get_parameter('piper.length_scale').get_parameter_value().double_value
            n_scale = self._node.get_parameter('piper.noise_scale').get_parameter_value().double_value
            nw_scale = self._node.get_parameter('piper.noise_w_scale').get_parameter_value().double_value
            vol = self._node.get_parameter('piper.volume').get_parameter_value().double_value
            s_id = self._node.get_parameter('piper.speaker_id').get_parameter_value().integer_value

            syn_config = SynthesisConfig(
                length_scale=l_scale,
                noise_scale=n_scale,
                noise_w_scale=nw_scale,
                volume=vol,
                speaker_id=s_id if self.voice.config.num_speakers > 1 else None,
                normalize_audio=True
            )

            start_time = time.time()
            all_audio_data = []

            for chunk in self.voice.synthesize(text, syn_config=syn_config):
                if hasattr(chunk, 'audio_int16_array'):
                    all_audio_data.append(np.array(chunk.audio_int16_array, dtype=np.int16))
                else:
                    all_audio_data.append(np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16))

            if not all_audio_data:
                return 0.0, None

            audio_array = np.concatenate(all_audio_data)
            duration = len(audio_array) / self.actual_sr

            audio_buffer_raw = io.BytesIO()
            sf.write(audio_buffer_raw, audio_array, self.actual_sr, format='WAV', subtype='PCM_16')
            audio_buffer_raw.seek(0)

            inf_time = time.time() - start_time
            self._logger.info(f"[Piper] Inference (CPU): {inf_time:.3f}s, Duration: {duration:.2f}s")
            return float(duration), audio_buffer_raw

        except Exception as e:
            self._logger.error(f"[Piper] Generation error: {e}")
            return 0.0, None