from rclpy.node import Node

import multiprocessing
import time
import io
import os
import wave
from typing import Tuple
from ament_index_python.packages import get_package_share_directory
from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile

from sobits_tts.include._base_tts import BaseTTSModel


class VoicevoxTTSModel(BaseTTSModel):
    def __init__(self, node: Node, sample_rate: int):
        super().__init__(node, sample_rate) 
        share_dir = get_package_share_directory('sobits_tts')
        package_path = os.path.join(os.path.abspath(os.path.join(share_dir, '..', '..', '..', '..')),
                                    'src', 'sobits_tts')
        
        onnx_path = os.path.join(package_path, 'install', 'voicevox_core', 'onnxruntime', 'lib', 'libvoicevox_onnxruntime.so.1.17.3')
        self.dict_path = os.path.join(package_path, 'install', 'voicevox_core', 'dict', 'open_jtalk_dic_utf_8-1.11')
        self.model_dir = os.path.join(package_path, 'install', 'voicevox_core', 'models', 'vvms')

        self._node.declare_parameter('voicevox.style_id', 14)
        self._node.declare_parameter('voicevox.model_file_num', '1.vvm')
        self._node.declare_parameter('voicevox.speed_scale', 1.0)
        self._node.declare_parameter('voicevox.pitch_scale', 0.0)
        self._node.declare_parameter('voicevox.intonation_scale', 1.0)
        self._node.declare_parameter('voicevox.volume_scale', 1.0)
        self._node.declare_parameter('voicevox.pre_phoneme_length', 0.1)
        self._node.declare_parameter('voicevox.post_phoneme_length', 0.1)
        self._node.declare_parameter('voicevox.output_sampling_rate', 24000)
        self._node.declare_parameter('voicevox.output_stereo', False)

        try:
            self.onnxruntime = Onnxruntime.load_once(filename=str(onnx_path))
            self._logger.info(f"Supported devices: {self.onnxruntime.supported_devices()}")
        except Exception as e:
            self._logger.error(f"Failed to initialize Onnxruntime: {e}")
            raise

    def generate_audio(self, text: str) -> Tuple[float, io.BytesIO]:
        try:
            synthesizer = Synthesizer(
                self.onnxruntime,
                OpenJtalk(str(self.dict_path)),
                acceleration_mode="AUTO",
                cpu_num_threads=max(multiprocessing.cpu_count(), 2),
            )
            self._logger.info(f"Using GPU: {synthesizer.is_gpu_mode}")

            style_id = self._node.get_parameter('voicevox.style_id').get_parameter_value().integer_value
            model_file_num = self._node.get_parameter('voicevox.model_file_num').get_parameter_value().string_value
            speed_scale = self._node.get_parameter('voicevox.speed_scale').get_parameter_value().double_value
            pitch_scale = self._node.get_parameter('voicevox.pitch_scale').get_parameter_value().double_value
            intonation_scale = self._node.get_parameter('voicevox.intonation_scale').get_parameter_value().double_value
            volume_scale = self._node.get_parameter('voicevox.volume_scale').get_parameter_value().double_value
            pre_phoneme_length = self._node.get_parameter('voicevox.pre_phoneme_length').get_parameter_value().double_value
            post_phoneme_length = self._node.get_parameter('voicevox.post_phoneme_length').get_parameter_value().double_value
            output_sampling_rate = self._node.get_parameter('voicevox.output_sampling_rate').get_parameter_value().integer_value
            output_stereo = self._node.get_parameter('voicevox.output_stereo').get_parameter_value().bool_value

            model_path = os.path.join(self.model_dir, model_file_num)

            with VoiceModelFile.open(model_path) as model:
                synthesizer.load_voice_model(model)

            query = synthesizer.create_audio_query(text, style_id)
            query.speed_scale = speed_scale
            query.pitch_scale = pitch_scale
            query.intonation_scale = intonation_scale
            query.volume_scale = volume_scale
            query.pre_phoneme_length = pre_phoneme_length
            query.post_phoneme_length = post_phoneme_length
            query.output_sampling_rate = output_sampling_rate
            query.output_stereo = output_stereo

            self._logger.info(f"test: {text}")
            start_time = time.time()

            wav = synthesizer.synthesis(query, style_id, enable_interrogative_upspeak=True)

            with wave.open(io.BytesIO(wav), 'rb') as wav_file:
                frames = wav_file.getnframes()
                play_time = frames / float(wav_file.getframerate())
            duration = time.time() - start_time
            self._logger.info(f"Synthesis time: {duration:.3f} seconds")
            self._logger.info(f"play_time: {play_time}")
            return play_time, io.BytesIO(wav)

        except Exception as e:
            self._logger.error(f"generate_audio failed: {e}", exc_info=True)
            raise
