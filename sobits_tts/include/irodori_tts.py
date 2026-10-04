from rclpy.node import Node

import atexit
import hashlib
import io
import json
import os
import re
import subprocess
import threading
import time
import numpy as np
import requests
import soundfile as sf
from scipy.signal import resample_poly
from typing import List, Tuple
from ament_index_python.packages import get_package_share_directory

from sobits_tts.include._base_tts import BaseTTSModel

DEFAULT_CHECKPOINT = 'Aratako/Irodori-TTS-v4.1-Small'
DEFAULT_DEVICE = 'cuda'
DEFAULT_PORT = 50070
DEFAULT_CACHE_DIR = os.path.expanduser('~/.sobits_tts/irodori/cache')
MAX_CHUNK_LENGTH = 80       # Irodoriは1回に30秒までしか生成できないため，長い文はこの文字数を目安に分割する
CHUNK_SILENCE_DURATION = 0.15


def get_package_path() -> str:
    share_dir = get_package_share_directory('sobits_tts')
    return os.path.join(os.path.abspath(os.path.join(share_dir, '..', '..', '..', '..')), 'src', 'sobits_tts')


def resolve_path(path: str) -> str:
    # 'package://<pkg>/<path>' 形式も受け付ける
    if not path:
        return ''
    if path.startswith('package://'):
        package, _, relative = path[len('package://'):].partition('/')
        path = os.path.join(get_package_share_directory(package), relative)
    return os.path.abspath(os.path.expanduser(path))


def split_text(text: str, max_chunk_length: int = MAX_CHUNK_LENGTH) -> List[str]:
    # 1文ずつに分ける(文の組み合わせが変わっても同じ文は同じキャッシュを使えるように)．
    # 長すぎる文は読点で分け，句読点だけの断片は捨てる
    chunks = []
    for sentence in re.split(r'(?<=[。！？!?\n])', text.strip()):
        current = ''
        for phrase in re.split(r'(?<=[、，,])', sentence):
            if current and len(current) + len(phrase) > max_chunk_length:
                chunks.append(current)
                current = ''
            current += phrase
        chunks.append(current)
    chunks = [c.strip() for c in chunks if re.sub(r'[\s。、，,．.！？!?]', '', c)]
    return chunks or [text]


def cache_key(text: str, ref_wav: str, caption: str, seed: int, checkpoint: str) -> str:
    # ステップ数はキーに含めない(事前生成した高品質な音声を本番でそのまま使うため)
    h = hashlib.sha1()
    if ref_wav:
        with open(ref_wav, 'rb') as f:
            h.update(hashlib.sha1(f.read()).digest())
    h.update(json.dumps([text, caption, int(seed), checkpoint], ensure_ascii=False).encode('utf-8'))
    return h.hexdigest()


class IrodoriServer:
    """専用venvでIrodoriのAPIサーバ(_irodori_server.py)を起動し，HTTPで合成を依頼する．"""

    def __init__(self, logger, port: int, checkpoint: str, device: str):
        self._logger = logger
        self.port = port
        self.checkpoint = checkpoint
        self.device = device
        self.base_url = f"http://127.0.0.1:{port}"
        self._server_process = None

        package_path = get_package_path()
        self.irodori_dir = os.path.join(package_path, 'install', 'irodori', 'Irodori-TTS')
        self.python_path = os.path.join(self.irodori_dir, '.venv', 'bin', 'python')
        self.server_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_irodori_server.py')

    def is_alive(self) -> bool:
        try:
            return requests.get(f"{self.base_url}/health", timeout=2).status_code == 200
        except Exception:
            return False

    def start(self, warmup_ref_wav: str, warmup_caption: str, warmup_num_steps: int, timeout: int = 300) -> bool:
        if self.is_alive():
            self._logger.info(f"[Irodori] Server is already running at {self.base_url}. Reusing it.")
            return True
        if not os.path.exists(self.python_path):
            self._logger.error(f"[Irodori] venv not found: {self.python_path}. Run install/irodori.sh first.")
            return False

        command = [
            self.python_path, self.server_path,
            "--irodori-dir", self.irodori_dir,
            "--checkpoint", self.checkpoint,
            "--device", self.device,
            "--port", str(self.port),
            "--warmup-ref-wav", warmup_ref_wav,
            "--warmup-caption", warmup_caption,
            "--warmup-num-steps", str(warmup_num_steps),
        ]
        self._logger.info(f"[Irodori] Launch command: {' '.join(command)}")
        self._server_process = subprocess.Popen(
            command,
            cwd=self.irodori_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        log_thread = threading.Thread(target=self._read_pipe, args=(self._server_process.stdout,))
        log_thread.daemon = True
        log_thread.start()
        return self._wait_for_server(timeout)

    def _read_pipe(self, pipe: io.TextIOBase):
        for line in iter(pipe.readline, ''):
            stripped_line = line.strip()
            if not stripped_line or 'WARNING! Reducing the sampling rate' in stripped_line or 'default SDR' in stripped_line:
                continue
            if 'Error' in stripped_line or 'Traceback' in stripped_line:
                self._logger.error(f"[Irodori Server] {stripped_line}")
            else:
                self._logger.info(f"[Irodori Server] {stripped_line}")
        pipe.close()

    def _wait_for_server(self, timeout: int) -> bool:
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self._server_process.poll() is not None:
                self._logger.error(f"[Irodori] Server exited with code {self._server_process.returncode}.")
                return False
            if self.is_alive():
                return True
            time.sleep(1)
        self._logger.error(f"[Irodori] Server did not start within {timeout}s.")
        return False

    def synthesize(self, text: str, ref_wav: str, caption: str, num_steps: int, seed: int) -> bytes:
        payload = {"text": text, "ref_wav": ref_wav, "caption": caption, "num_steps": int(num_steps), "seed": int(seed)}
        response = requests.post(f"{self.base_url}/synthesize", data=json.dumps(payload),
                                 headers={"Content-Type": "application/json"}, timeout=120)
        response.raise_for_status()
        return response.content

    def stop(self):
        # 自分で起動したサーバのみ止める
        if self._server_process and self._server_process.poll() is None:
            self._server_process.terminate()
            try:
                self._server_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self._server_process.kill()
        self._server_process = None


class IrodoriTTSModel(BaseTTSModel):
    # Irodoriの出力は48kHz．24kHzに落とすと音が荒れるため，tts_action_serverはこの値でミキサーを初期化する
    output_sample_rate = 48000

    def __init__(self, node: Node, sample_rate: int):
        super().__init__(node, sample_rate)

        self._node.declare_parameter('irodori.ref_wav', '')
        self._node.declare_parameter('irodori.caption', '')
        self._node.declare_parameter('irodori.num_steps', 16)
        self._node.declare_parameter('irodori.seed', 0)
        self._node.declare_parameter('irodori.checkpoint', DEFAULT_CHECKPOINT)
        self._node.declare_parameter('irodori.device', DEFAULT_DEVICE)
        self._node.declare_parameter('irodori.port', DEFAULT_PORT)
        self._node.declare_parameter('irodori.cache_dir', DEFAULT_CACHE_DIR)

        self.checkpoint = self._node.get_parameter('irodori.checkpoint').get_parameter_value().string_value
        device = self._node.get_parameter('irodori.device').get_parameter_value().string_value
        port = self._node.get_parameter('irodori.port').get_parameter_value().integer_value
        self.cache_dir = resolve_path(self._node.get_parameter('irodori.cache_dir').get_parameter_value().string_value)
        os.makedirs(self.cache_dir, exist_ok=True)

        ref_wav, caption, num_steps, _ = self._get_voice_params()
        self.server = IrodoriServer(self._logger, port, self.checkpoint, device)
        atexit.register(self.server.stop)
        if not self.server.start(ref_wav, caption, num_steps):
            self.server.stop()
            raise RuntimeError("Irodori TTS initialization failed.")

        YELLOW = '\033[93m'
        ENDC = '\033[0m'
        self._logger.info(f"{YELLOW}[Irodori] Server initialized. Cache: {self.cache_dir}{ENDC}")

    def _get_voice_params(self):
        ref_wav = resolve_path(self._node.get_parameter('irodori.ref_wav').get_parameter_value().string_value)
        caption = self._node.get_parameter('irodori.caption').get_parameter_value().string_value
        num_steps = self._node.get_parameter('irodori.num_steps').get_parameter_value().integer_value
        seed = self._node.get_parameter('irodori.seed').get_parameter_value().integer_value
        return ref_wav, caption, num_steps, seed

    def generate_audio(self, text: str) -> Tuple[float, io.BytesIO]:
        try:
            ref_wav, caption, num_steps, seed = self._get_voice_params()

            start_time = time.time()
            audio_chunks, num_cached, actual_sr = [], 0, None
            for chunk in split_text(text):
                cache_path = os.path.join(self.cache_dir, f"{cache_key(chunk, ref_wav, caption, seed, self.checkpoint)}.wav")
                if os.path.exists(cache_path):
                    num_cached += 1
                else:
                    wav_bytes = self.server.synthesize(chunk, ref_wav, caption, num_steps, seed)
                    with open(cache_path + '.tmp', 'wb') as f:
                        f.write(wav_bytes)
                    os.replace(cache_path + '.tmp', cache_path)
                audio, actual_sr = sf.read(cache_path, dtype='float32')
                if audio_chunks:
                    audio_chunks.append(np.zeros(int(CHUNK_SILENCE_DURATION * actual_sr), dtype=np.float32))
                audio_chunks.append(audio)

            audio = np.concatenate(audio_chunks)
            if actual_sr != self.output_sample_rate:
                g = np.gcd(actual_sr, self.output_sample_rate)
                audio = resample_poly(audio, self.output_sample_rate // g, actual_sr // g).astype(np.float32)
            play_time = len(audio) / float(self.output_sample_rate)

            inference_time = time.time() - start_time
            self._logger.info(f"[Irodori] Inference time: {inference_time:.3f}s for {len(text)} chars "
                              f"({num_cached}/{len(audio_chunks) // 2 + 1} chunks from cache)")

            audio_buffer = io.BytesIO()
            sf.write(audio_buffer, np.clip(audio, -1.0, 1.0), self.output_sample_rate, format='WAV', subtype='PCM_16')
            audio_buffer.seek(0)
            return play_time, audio_buffer

        except Exception as e:
            self._logger.error(f"[Irodori] Generation error: {e}")
            return 0.0, None

    def __del__(self):
        if hasattr(self, 'server'):
            self.server.stop()
