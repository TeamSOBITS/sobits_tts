from rclpy.node import Node

from kokoro import KPipeline
import numpy as np
import torch
import soundfile as sf
import io
import os
import sys
import atexit
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

        self.lang_code = self._node.get_parameter('kokoro.lang_code').get_parameter_value().string_value
        self.voice = self._node.get_parameter('kokoro.voice').get_parameter_value().string_value
        self.speech_speed = self._node.get_parameter('kokoro.speech_speed').get_parameter_value().double_value
        self.split_regex = self._node.get_parameter('kokoro.split_regex').get_parameter_value().string_value

        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self._logger.debug(f"KokoroTTS using device: {self.device}")

        HF_REPO_NAME = "hexgrad/Kokoro-82M"
        HF_CACHE_ROOT_PATH = os.path.join("~", ".cache", "huggingface")
        resolved_cache_root = os.path.expanduser(HF_CACHE_ROOT_PATH)
        repo_dir = os.path.join(resolved_cache_root, "hub", f"models--{HF_REPO_NAME.replace('/', '--')}")
        is_local_cache_found = os.path.isdir(repo_dir) and os.path.isdir(os.path.join(repo_dir, "snapshots"))

        if is_local_cache_found:
            self._logger.info("Kokoro TTS: Local cache found. Forcing local-only load.")
            
            os.environ['HF_HUB_OFFLINE'] = '1'
            os.environ['TRANSFORMERS_OFFLINE'] = '1'
            
            def cleanup_env_vars(logger):
                if 'HF_HUB_OFFLINE' in os.environ:
                    del os.environ['HF_HUB_OFFLINE']
                    logger.info("Cleaned up HF_HUB_OFFLINE environment variable.")
                if 'TRANSFORMERS_OFFLINE' in os.environ:
                    del os.environ['TRANSFORMERS_OFFLINE']
                    logger.info("Cleaned up TRANSFORMERS_OFFLINE environment variable.")
            atexit.register(cleanup_env_vars, self._logger)
            
            if hasattr(fd, 'hf_hub_download') and not getattr(fd.hf_hub_download, '_is_patched', False):
                original_hf_hub_download = fd.hf_hub_download
            else:
                original_hf_hub_download = hf_hub_download

            def offline_hf_hub_download_wrapper(*args, **kwargs):
                kwargs['local_files_only'] = True
                return original_hf_hub_download(*args, **kwargs)
            
            offline_hf_hub_download_wrapper._is_patched = True

            patched_count = 0
            for module_name, module in list(sys.modules.items()):
                if module_name.startswith('kokoro') or module_name == 'kokoro':
                    if hasattr(module, 'hf_hub_download'):
                        setattr(module, 'hf_hub_download', offline_hf_hub_download_wrapper)
                        patched_count += 1
            
            fd.hf_hub_download = offline_hf_hub_download_wrapper
            
            self._logger.info(f"Applied offline patch to {patched_count} kokoro modules and huggingface_hub.")
            
        else:
            self._logger.warn("Local model cache not found. Attempting online download.")
            if 'HF_HUB_OFFLINE' in os.environ: del os.environ['HF_HUB_OFFLINE']
            if 'TRANSFORMERS_OFFLINE' in os.environ: del os.environ['TRANSFORMERS_OFFLINE']

        try:
            self.pipeline = KPipeline(
                lang_code=self.lang_code, 
                device=self.device, 
            )
            self._logger.info("Kokoro TTS initialized successfully.")
        except Exception as e:
            self._logger.error(f"Failed to initialize Kokoro TTS: {e}")
            raise 

    def generate_audio(self, text: str) -> Tuple[float, io.BytesIO]:
        combined_audio_chunks = []
        total_samples = 0
        
        try:
            for i, result in enumerate(
                self.pipeline(
                    text, 
                    voice=self.voice, 
                    speed=self.speech_speed, 
                    split_pattern=self.split_regex
                )
            ):
                audio_chunk = result.audio

                if isinstance(audio_chunk, torch.Tensor):
                    audio_chunk = audio_chunk.cpu().numpy()
                
                if audio_chunk.ndim == 1:
                    final_chunk = audio_chunk
                else:
                    self._logger.error(f"Unsupported audio chunk shape.")
                    return 0.0, None

                combined_audio_chunks.append(final_chunk)
                total_samples += final_chunk.shape[0]
            
        except RuntimeError as e:
            self._logger.error(f"Runtime error during Kokoro KPipeline processing: {e}")
            return 0.0, None
        except Exception as e:
            self._logger.error(f"An unexpected error occurred during Kokoro audio generation: {e}")
            return 0.0, None

        if not combined_audio_chunks:
            self._logger.warn("No audio chunks generated by Kokoro TTS for the given text.")
            return 0.0, None

        try:
            combined_audio = np.concatenate(combined_audio_chunks, axis=0)
        except ValueError as e:
             self._logger.error(f"Error concatenating audio chunks: {e}")
             return 0.0, None

        play_time = float(total_samples) / self._sample_rate

        if play_time <= 0:
            self._logger.warn(f"Kokoro: Calculated play_time is zero or negative ({play_time:.2f}s).")
            return 0.0, None

        try:
            buffer = io.BytesIO()
            sf.write(buffer, combined_audio, self._sample_rate, format='WAV', subtype='PCM_16')
            buffer.seek(0)
            return play_time, buffer
        except Exception as e:
            self._logger.error(f"Error writing audio to buffer: {e}")
            return 0.0, None