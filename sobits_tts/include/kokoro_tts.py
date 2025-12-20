from rclpy.node import Node

from kokoro import KPipeline
import numpy as np
import torch
import soundfile as sf
import io
import os
import sys
import atexit
import gc
from huggingface_hub import hf_hub_download
import huggingface_hub.file_download as fd

from typing import Tuple
from sobits_tts.include._base_tts import BaseTTSModel

class KokoroTTSModel(BaseTTSModel):
    def __init__(self, node: Node, sample_rate: int):
        super().__init__(node, sample_rate) 

        self._node.declare_parameter('kokoro.lang_code', 'a')
        self._node.declare_parameter('kokoro.voice', 'af_heart')
        self._node.declare_parameter('kokoro.speech_speed', 1.0)
        self._node.declare_parameter('kokoro.split_regex', r'[\n,.!?、。！？]+')
        self._node.declare_parameter('kokoro.device', '') # デフォルト空

        self.lang_code = self._node.get_parameter('kokoro.lang_code').get_parameter_value().string_value
        self.voice = self._node.get_parameter('kokoro.voice').get_parameter_value().string_value
        self.speech_speed = self._node.get_parameter('kokoro.speech_speed').get_parameter_value().double_value
        self.split_regex = self._node.get_parameter('kokoro.split_regex').get_parameter_value().string_value
        
        device_param = self._node.get_parameter('kokoro.device').get_parameter_value().string_value
        if not device_param:
            self.target_device = "cuda:0" if torch.cuda.is_available() else "cpu"
        else:
            self.target_device = device_param

        self._original_hf_download = fd.hf_hub_download
        atexit.register(self._cleanup_env_vars)

        self._logger.info("Step 1: Attempting offline initialization...")
        success = self._try_init_tts(offline_mode=True)

        if not success:
            self._logger.warn("Offline initialization failed. Step 2: Retrying in Online mode...")
            success = self._try_init_tts(offline_mode=False)
            
            if success:
                self._logger.info("Online initialization succeeded.")
                self._apply_offline_patch(True)
            else:
                self._logger.fatal("Failed to initialize Kokoro TTS.")
                raise RuntimeError("Kokoro TTS initialization failed.")
        
        actual_device = self.pipeline.model.device
        self._logger.info(f"KokoroTTS initialized on actual device: {actual_device}")

    def _try_init_tts(self, offline_mode: bool) -> bool:
        try:
            self._apply_offline_patch(offline_mode)
            self.pipeline = KPipeline(lang_code=self.lang_code, device=self.target_device)
            return True
        except Exception as e:
            self._logger.error(f"Init error (offline={offline_mode}): {e}")
            if hasattr(self, 'pipeline'): del self.pipeline
            gc.collect()
            if torch.cuda.is_available():
                try:
                    with torch.cuda.device(self.target_device if 'cuda' in self.target_device else 0):
                        torch.cuda.empty_cache()
                except:
                    pass
            return False

    def _apply_offline_patch(self, enable: bool):
        if enable:
            os.environ['HF_HUB_OFFLINE'] = '1'
            os.environ['TRANSFORMERS_OFFLINE'] = '1'
            local_files_only = True
        else:
            os.environ.pop('HF_HUB_OFFLINE', None)
            os.environ.pop('TRANSFORMERS_OFFLINE', None)
            local_files_only = False

        def wrapper(*args, **kwargs):
            kwargs['local_files_only'] = local_files_only
            return self._original_hf_download(*args, **kwargs)

        fd.hf_hub_download = wrapper
        for module_name, module in list(sys.modules.items()):
            if module_name.startswith('kokoro') or module_name == 'kokoro':
                if hasattr(module, 'hf_hub_download'):
                    setattr(module, 'hf_hub_download', wrapper)
        
        mode = "ENABLED (Offline)" if enable else "DISABLED (Online)"
        self._logger.info(f"Offline patch {mode}")

    def generate_audio(self, text: str) -> Tuple[float, io.BytesIO]:
        try:
            return self._execute_pipeline(text)
        except Exception as e:
            err_msg = str(e)
            if "local_files_only" in err_msg or "disk cache" in err_msg or "Offline" in err_msg:
                self._logger.warn(f"Missing resources for text: [{text}]. Switching to Online mode temporarily...")
                try:
                    self._apply_offline_patch(False) 
                    result = self._execute_pipeline(text)
                    self._apply_offline_patch(True)  
                    self._logger.info("Successfully downloaded missing resources and generated audio.")
                    return result
                except Exception as e_retry:
                    self._logger.error(f"Online retry failed: {e_retry}")
            else:
                self._logger.error(f"Unexpected generation error: {e}")
        
        return 0.0, None

    def _execute_pipeline(self, text: str) -> Tuple[float, io.BytesIO]:
        combined_audio_chunks = []
        total_samples = 0
        
        for result in self.pipeline(
            text, voice=self.voice, speed=self.speech_speed, split_pattern=self.split_regex
        ):
            audio_chunk = result.audio
            if isinstance(audio_chunk, torch.Tensor):
                audio_chunk = audio_chunk.cpu().numpy()
            
            if audio_chunk.ndim == 1:
                combined_audio_chunks.append(audio_chunk)
                total_samples += audio_chunk.shape[0]

        if not combined_audio_chunks:
            return 0.0, None

        combined_audio = np.concatenate(combined_audio_chunks, axis=0)
        play_time = float(total_samples) / self._sample_rate

        buffer = io.BytesIO()
        sf.write(buffer, combined_audio, self._sample_rate, format='WAV', subtype='PCM_16')
        buffer.seek(0)
        return play_time, buffer

    def _cleanup_env_vars(self):
        for var in ['HF_HUB_OFFLINE', 'TRANSFORMERS_OFFLINE']:
            os.environ.pop(var, None)
        if hasattr(self, '_logger'):
            self._logger.info("Environment variables cleaned up.")