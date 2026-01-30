from rclpy.node import Node

from supertonic import TTS
import numpy as np
import soundfile as sf
import io
import os
import atexit
import gc
import time
import onnxruntime as ort

from typing import Tuple
from ament_index_python.packages import get_package_share_directory
from sobits_tts.include._base_tts import BaseTTSModel

class SupertonicTTSModel(BaseTTSModel):
    _env_registered = False

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

        available_providers = ort.get_available_providers()
        has_cuda = "CUDAExecutionProvider" in available_providers

        if device_param == 'cuda' or device_param == 'gpu':
            self.target_gpu = True
        elif device_param == 'cpu':
            self.target_gpu = False
        else:
            self.target_gpu = has_cuda

        if not SupertonicTTSModel._env_registered:
            self._old_cuda_visible = os.environ.get("CUDA_VISIBLE_DEVICES")
            atexit.register(self._cleanup_env)
            SupertonicTTSModel._env_registered = True

        if not self.target_gpu:
            os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
            self._logger.info("[Supertonic] Mode: Forced CPU")
        else:
            if "CUDA_VISIBLE_DEVICES" in os.environ:
                del os.environ["CUDA_VISIBLE_DEVICES"]
            self._logger.info("[Supertonic] Mode: GPU (CUDA)")

        opt_path = "/opt/supertonic_model"
        
        if os.path.exists(opt_path) and any(os.scandir(opt_path)):
            self.base_path = opt_path
            self._logger.info(f"[Supertonic] Using model from system path: {self.base_path}")
        else:
            self.base_path = os.path.expanduser("~/colcon_ws/src/sobits_tts/install/supertonic")
            self._logger.warn(f"[Supertonic] /opt path not found. Falling back to: {self.base_path}")
        
        try:
            self.supertonic_tts = TTS(
                model_dir=self.base_path,
                auto_download=False,
                intra_op_num_threads=intra if intra > 0 else None,
                inter_op_num_threads=inter if inter > 0 else None
            )
            self._logger.info(f"[Supertonic] Successfully initialized from: {self.base_path}")
        except Exception as e:
            self._cleanup_env()
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

    def _cleanup_env(self):
        if hasattr(self, '_old_cuda_visible'):
            if self._old_cuda_visible is None:
                os.environ.pop("CUDA_VISIBLE_DEVICES", None)
            else:
                os.environ["CUDA_VISIBLE_DEVICES"] = self._old_cuda_visible
            print("[Supertonic] Environment variables restored.")

    def __del__(self):
        if hasattr(self, 'supertonic_tts'):
            del self.supertonic_tts
        gc.collect()