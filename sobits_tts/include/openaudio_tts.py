from rclpy.node import Node
from typing import Tuple
import requests
import base64
import json
import io
import time
import wave
import os
import subprocess
import threading
import re
import site
import sys
from ament_index_python.packages import get_package_share_directory

from sobits_tts.include._base_tts import BaseTTSModel

class OpenaudioTTSModel(BaseTTSModel):
    def __init__(self, node: Node, sample_rate: int):
        super().__init__(node, sample_rate)
        share_dir = get_package_share_directory('sobits_tts')
        package_path = os.path.join(os.path.abspath(os.path.join(share_dir, '..', '..', '..', '..')),
                                        'src', 'sobits_tts')
        self.api_server_path = self._find_api_server_path()
        self.llama_checkpoint_path = os.path.join(package_path, 'install', 'checkpoints', 'openaudio-s1-mini')
        self.decoder_checkpoint_path = os.path.join(package_path, 'install', 'checkpoints', 'openaudio-s1-mini', 'codec.pth')
        self.decoder_config_name = 'modded_dac_vq'
        self.format_param = 'wav'
        self.streaming_api_param = False

        self._node.declare_parameter('openaudio_tts.listen_address', '0.0.0.0:8080')
        self._node.declare_parameter('openaudio_tts.use_half_precision', True)
        self._node.declare_parameter('openaudio_tts.device', 'cuda')
        self._node.declare_parameter('openaudio_tts.compile_model', False)
        self._node.declare_parameter('openaudio_tts.max_text_length', 256)

        self._node.declare_parameter('openaudio_tts.chunk_length', 200)
        self._node.declare_parameter('openaudio_tts.reference_audio_path', os.path.join(package_path, 'soundfile', 'input.wav'))
        self._node.declare_parameter('openaudio_tts.reference_text', "")
        self._node.declare_parameter('openaudio_tts.reference_id', None)
        self._node.declare_parameter('openaudio_tts.seed', None)
        self._node.declare_parameter('openaudio_tts.use_memory_cache', True)
        self._node.declare_parameter('openaudio_tts.normalize', True)
        self._node.declare_parameter('openaudio_tts.max_new_tokens', 1024)
        self._node.declare_parameter('openaudio_tts.top_p', 0.8)
        self._node.declare_parameter('openaudio_tts.repetition_penalty', 1.1)
        self._node.declare_parameter('openaudio_tts.temperature', 0.8)

        self.listen_address = self._node.get_parameter('openaudio_tts.listen_address').value
        self.use_half_precision = self._node.get_parameter('openaudio_tts.use_half_precision').value
        self.device = self._node.get_parameter('openaudio_tts.device').value
        self.compile_model = self._node.get_parameter('openaudio_tts.compile_model').value
        self.max_text_length = self._node.get_parameter('openaudio_tts.max_text_length').value

        base_url = f"http://{self.listen_address.split(':')[0]}:{self.listen_address.split(':')[1]}"
        self.full_api_url = f"{base_url}/v1/tts"

        self.headers = {
            "accept": "audio/wav",
            "Content-Type": "application/json",
        }
        self._initialized_successfully = False
        self._server_process = None

        self._logger.info(f"Starting OpenAudioTTS server at {self.listen_address}...")
        server_thread = threading.Thread(target=self._launch_server)
        server_thread.daemon = True
        server_thread.start()

        if self._wait_for_server():
            self._initialized_successfully = True
            YELLOW = '\033[93m'
            ENDC = '\033[0m'
            self._logger.info(f"{YELLOW}OpenAudioTTS server initialized. URL: {base_url}{ENDC}")
        else:
            self._logger.error("Failed to initialize OpenAudioTTS server.")

    def _find_api_server_path(self):
        site_packages_paths = site.getsitepackages()
        if site.ENABLE_USER_SITE:
            site_packages_paths.append(site.getuserbase() + '/lib/python' + sys.version[:3] + '/site-packages')
        all_possible_paths = list(set(list(sys.path) + site_packages_paths))

        for sp_path in all_possible_paths:
            candidate_path = os.path.join(sp_path, 'tools', 'api_server.py')
            if os.path.exists(candidate_path):
                self._node.get_logger().info(f"Found api_server.py at: {candidate_path}")
                return candidate_path
        self._node.get_logger().error("api_server.py not found.")
        return "/home/sobits/.local/lib/python3.10/site-packages/tools/api_server.py"

    def _launch_server(self):
        command = [
            "python3",
            self.api_server_path,
            "--listen", self.listen_address,
            "--llama-checkpoint-path", self.llama_checkpoint_path,
            "--decoder-checkpoint-path", self.decoder_checkpoint_path,
            "--decoder-config-name", self.decoder_config_name,
            "--device", self.device,
            "--max-text-length", str(self.max_text_length),
        ]

        if self.use_half_precision:
            command.append("--half")
            self._logger.info("Using FP16 half-precision mode.")

        if self.compile_model:
            command.append("--compile")
            self._logger.info("Enabling model compilation (torch.compile).")

        try:
            self._logger.info(f"Launch command: {' '.join(command)}")
            self._server_process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            stdout_thread = threading.Thread(target=self._read_pipe, args=(self._server_process.stdout, "stdout"))
            stderr_thread = threading.Thread(target=self._read_pipe, args=(self._server_process.stderr, "stderr"))
            stdout_thread.daemon = True
            stderr_thread.daemon = True
            stdout_thread.start()
            stderr_thread.start()

        except Exception as e:
            self._logger.error(f"Failed to launch OpenAudioTTS server: {e}")

    def _read_pipe(self, pipe: io.TextIOBase, log_source_type: str):
        for line in iter(pipe.readline, ''):
            stripped_line = line.strip()
            if not stripped_line:
                self._logger.debug(f"[OpenAudioTTS Server] (empty line from pipe)")
                continue
            if "| INFO" in stripped_line or \
               (stripped_line.startswith("INFO:") and ("Uvicorn" in stripped_line or "Started server process" in stripped_line or "Waiting for application startup" in stripped_line or "Application startup complete" in stripped_line)) or \
               re.match(r'^\d+%\|.*', stripped_line):
                self._logger.info(f"[OpenAudioTTS Server] {stripped_line}")
            elif "| WARNING" in stripped_line or "UserWarning:" in stripped_line:
                self._logger.warn(f"[OpenAudioTTS Server] {stripped_line}")
            elif "| ERROR" in stripped_line or "| CRITICAL" in stripped_line:
                self._logger.error(f"[OpenAudioTTS Server] {stripped_line}")
            else:
                if log_source_type == "stdout":
                    self._logger.info(f"[OpenAudioTTS Server] {stripped_line}")
                elif log_source_type == "stderr":
                    self._logger.error(f"[OpenAudioTTS Server] {stripped_line}")
                else:
                    self._logger.debug(f"[OpenAudioTTS Server] {stripped_line}")
        pipe.close()

    def _wait_for_server(self, timeout: int = 60):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                check_url = self.full_api_url.replace("/v1/tts", "")
                response = requests.get(check_url, timeout=5)
                if response.status_code in (200, 405):
                    return True
            except Exception:
                time.sleep(1)
        return False

    def generate_audio(self, text: str) -> Tuple[float, io.BytesIO]:
        if not self._initialized_successfully:
            self._logger.error("OpenAudioTTS server not initialized.")
            return 0.0, None

        self.reference_audio_path = os.path.abspath(self._node.get_parameter('openaudio_tts.reference_audio_path').value)
        encoded_ref_audio = None
        if self.reference_audio_path:
            try:
                with open(self.reference_audio_path, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                    encoded_ref_audio = base64.b64encode(audio_bytes).decode('utf-8')
            except Exception as e:
                self._logger.warning(f"Failed to load reference audio: {e}")
        self.reference_text = self._node.get_parameter('openaudio_tts.reference_text').value
        
        references_payload = []
        if encoded_ref_audio:
            ref_entry = {
                "audio": encoded_ref_audio,
                "text": self.reference_text
            }
            references_payload.append(ref_entry)
        self.reference_id = self._node.get_parameter('openaudio_tts.reference_id').value
        self.reference_id = None if self.reference_id == 'None' else self.reference_id
        self.chunk_length = self._node.get_parameter('openaudio_tts.chunk_length').value
        self.seed = self._node.get_parameter('openaudio_tts.seed').value
        self.seed = None if self.seed in ('None', None) else int(self.seed)
        self.use_memory_cache = self._node.get_parameter('openaudio_tts.use_memory_cache').value
        self.use_memory_cache = "on" if self.use_memory_cache else "off"
        self.normalize = self._node.get_parameter('openaudio_tts.normalize').value
        self.max_new_tokens = self._node.get_parameter('openaudio_tts.max_new_tokens').value
        self.top_p = self._node.get_parameter('openaudio_tts.top_p').value
        self.repetition_penalty = self._node.get_parameter('openaudio_tts.repetition_penalty').value
        self.temperature = self._node.get_parameter('openaudio_tts.temperature').value

        payload = {
            "text": text,
            "chunk_length": self.chunk_length,
            "format": self.format_param,
            "references": references_payload,
            "reference_id": self.reference_id,
            "seed": self.seed,
            "use_memory_cache": self.use_memory_cache,
            "normalize": self.normalize,
            "streaming": self.streaming_api_param,
            "max_new_tokens": self.max_new_tokens,
            "top_p": self.top_p,
            "repetition_penalty": self.repetition_penalty,
            "temperature": self.temperature
        }

        try:
            response = requests.post(self.full_api_url, headers=self.headers, data=json.dumps(payload), timeout=120)
            response.raise_for_status()
        except Exception as e:
            self._logger.error(f"Audio generation failed: {e}")
            return 0.0, None

        final_wav_bytes = response.content
        try:
            with wave.open(io.BytesIO(final_wav_bytes), "rb") as wf:
                play_time = wf.getnframes() / wf.getframerate()
        except wave.Error:
            return 0.0, None

        buffer = io.BytesIO(final_wav_bytes)
        return play_time, buffer