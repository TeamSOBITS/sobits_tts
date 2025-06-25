import rclpy
from rclpy.node import Node
from sobits_tts.include._base_tts import BaseTTSModel
import subprocess
import codecs
import os
import soundfile as sf
import wave
import io
import tempfile
from typing import Tuple

class OpenpicoTTSModel(BaseTTSModel): # Pを小文字に変更
    """
    Open JTalk と Pico TTS を使用して音声合成を行うTTSモデルクラス。
    BaseTTSModelを継承。
    """
    def __init__(self, node: Node, sample_rate: int):
        super().__init__(node, sample_rate)

        # ROSパラメータの宣言と取得（プレフィックス: openpico.）
        self._node.declare_parameter('openpico.voice_data_ja', '/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice')
        self._node.declare_parameter('openpico.language', 'ja')
        self._node.declare_parameter('openpico.dic_path_ja', '/var/lib/mecab/dic/open-jtalk/naist-jdic')
        self._node.declare_parameter('openpico.open_jtalk_cmd', 'open_jtalk')
        self._node.declare_parameter('openpico.pico2wave_cmd', 'pico2wave')

        self.voice_data_ja = self._node.get_parameter('openpico.voice_data_ja').get_parameter_value().string_value
        self.language = self._node.get_parameter('openpico.language').get_parameter_value().string_value
        self.dic_path_ja = self._node.get_parameter('openpico.dic_path_ja').get_parameter_value().string_value
        self.open_jtalk_cmd = self._node.get_parameter('openpico.open_jtalk_cmd').get_parameter_value().string_value
        self.pico2wave_cmd = self._node.get_parameter('openpico.pico2wave_cmd').get_parameter_value().string_value

        # 外部コマンドとファイルパスの存在チェック
        self._check_deps()
        self._logger.info(f"OpenPicoTTSModel initialized. Default language: {self.language}")

    def _check_deps(self):
        """依存する外部コマンドとファイルの存在をチェックする"""
        deps = {
            self.open_jtalk_cmd: "Open JTalk",
            self.pico2wave_cmd: "Pico TTS (libttspico-utils)",
        }
        for cmd, name in deps.items():
            if subprocess.run(['which', cmd], capture_output=True).returncode != 0:
                self._logger.fatal(f"Command '{cmd}' ({name}) not found. Please install it.")
                raise RuntimeError(f"Required command '{cmd}' not found.")
        
        paths = {
            self.dic_path_ja: "Open JTalk dictionary",
            self.voice_data_ja: "Open JTalk voice data"
        }
        for path, name in paths.items():
            if not os.path.exists(path):
                self._logger.fatal(f"{name} not found at '{path}'.")
                raise RuntimeError(f"{name} not found.")

    def _execute_tts_command(self, cmd_list: list, input_text: str = None) -> Tuple[bytes, bytes]:
        """TTSコマンドを実行し、stdoutとstderrを返すヘルパー"""
        try:
            p = subprocess.Popen(cmd_list, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate(input=input_text.encode('utf-8') if input_text else None)
            if p.returncode != 0:
                self._logger.error(f"TTS command failed with exit code {p.returncode}.")
                self._logger.error(f"Stdout: {stdout.decode().strip()}")
                self._logger.error(f"Stderr: {stderr.decode().strip()}")
                raise subprocess.CalledProcessError(p.returncode, cmd_list, stdout, stderr)
            return stdout, stderr
        except FileNotFoundError:
            self._logger.error(f"Command '{cmd_list[0]}' not found. Is it installed?")
            raise
        except Exception as e:
            self._logger.error(f"Error executing command '{cmd_list[0]}': {e}")
            raise

    def _get_audio_info(self, filepath: str) -> float:
        """WAVファイルの再生時間を取得するヘルパー"""
        try:
            if filepath.endswith('.wav'): # Pico TTS (soundfile) / Open JTalk (wave)
                if self.language == 'en': # Pico TTS uses soundfile
                     with sf.SoundFile(filepath, 'r') as f:
                        return float(len(f)) / float(f.samplerate)
                else: # Open JTalk uses wave
                    with wave.open(filepath, "r") as wf:
                        return float(wf.getnframes()) / wf.getframerate()
            return 0.0 # Unknown file type or error
        except Exception as e:
            self._logger.error(f"Error reading audio file '{filepath}': {e}")
            return 0.0

    def generate_audio(self, text: str) -> Tuple[float, io.BytesIO]:
        """
        BaseTTSModelの抽象メソッドを実装。
        設定された言語に基づいてOpen JTalkまたはPico TTSを呼び出し、
        音声データをio.BytesIOとして返す。
        """
        play_time = 0.0
        audio_buffer = None
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            output_filepath = tmp_file.name
        
        try:
            if self.language == "en":
                # Pico TTS (pico2wave)
                speech_text = codecs.decode(str(text).encode('utf-8'))
                if not speech_text.strip(): return 0.0, None # 空白チェック
                cmd = [self.pico2wave_cmd, '-w', output_filepath, speech_text]
                self._execute_tts_command(cmd) # stderr, stdout は無視

            elif self.language == "ja":
                # Open JTalk
                cmd = [
                    self.open_jtalk_cmd, '-x', self.dic_path_ja, '-m', self.voice_data_ja,
                    '-a', '0.5', '-b', '0.3', '-r', '1.0', '-ow', output_filepath,
                    '-ot', os.path.splitext(output_filepath)[0] + ".log"
                ]
                self._execute_tts_command(cmd, input_text=text)

            else:
                self._logger.error(f"Unsupported language: {self.language}")
                return 0.0, None

            # 音声ファイルの再生時間取得とバッファへの読み込み
            play_time = self._get_audio_info(output_filepath)
            if play_time > 0:
                with open(output_filepath, 'rb') as f:
                    audio_buffer = io.BytesIO(f.read())
                audio_buffer.seek(0)
            else:
                self._logger.error(f"Generated audio is invalid or empty for language '{self.language}'.")
                return 0.0, None

        except subprocess.CalledProcessError: # 外部コマンド実行失敗時
            return 0.0, None
        except Exception as e: # その他のエラー
            self._logger.error(f"An unexpected error occurred during audio generation: {e}", exc_info=True)
            return 0.0, None
        finally:
            if os.path.exists(output_filepath):
                os.remove(output_filepath)

        return play_time, audio_buffer