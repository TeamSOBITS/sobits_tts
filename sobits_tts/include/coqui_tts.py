import rclpy
from rclpy.node import Node
import requests
import io
import wave # WAVファイルのヘッダを読み取って再生時間を計算するため
import os # style_wav のパス処理のため
from typing import Tuple
import traceback # エラーログ用

# BaseTTSModelを継承するため、その定義をインポート
from sobits_tts.include._base_tts import BaseTTSModel

class CoquiTTSModel(BaseTTSModel):
    """
    Coqui TTS (TTSサーバーAPI経由) を使用して音声合成を行うTTSモデルクラス。
    BaseTTSModelを継承。
    """
    def __init__(self, node: Node, sample_rate: int):
        # BaseTTSModelのコンストラクタを呼び出す
        super().__init__(node, sample_rate)

        # Coqui TTS 固有のROSパラメータをここで宣言・取得
        # パラメータ名にはモデル固有のプレフィックス 'coqui.' をつける
        self._node.declare_parameter('coqui.url', 'http://localhost:5002')
        self._node.declare_parameter('coqui.add_stop_char', True)
        self._node.declare_parameter('coqui.speaker_id', 'p225')
        self._node.declare_parameter('coqui.language_id', '')
        self._node.declare_parameter('coqui.style_wav', '') # TTSサーバーから参照可能なパスまたはURL
        
        # 宣言したパラメータの値を取得
        self.url = self._node.get_parameter('coqui.url').get_parameter_value().string_value
        self.add_stop_char = self._node.get_parameter('coqui.add_stop_char').get_parameter_value().bool_value
        self.speaker_id = self._node.get_parameter('coqui.speaker_id').get_parameter_value().string_value
        self.language_id = self._node.get_parameter('coqui.language_id').get_parameter_value().string_value
        self.style_wav = self._node.get_parameter('coqui.style_wav').get_parameter_value().string_value
        
        self.VALID_END_OF_PHRASE = ['.', ';', '!', '?']

        self._logger.info(f"CoquiTTSModel initialized. URL: {self.url}, Speaker ID: {self.speaker_id}")
        self._initialized_successfully = True # 初期化成功フラグ

    def _end_text(self, text: str) -> str:
        """
        必要に応じてテキストの最後に句読点を追加するヘルパーメソッド。
        """
        if self.add_stop_char and text and text[-1] not in self.VALID_END_OF_PHRASE:
            text += "."
        return text

    def generate_audio(self, text: str) -> Tuple[float, io.BytesIO]:
        """
        BaseTTSModelの抽象メソッドを実装。
        Coqui TTSサーバーのAPIを呼び出し、音声データをio.BytesIOとして返す。
        """
        if not self._initialized_successfully:
            self._logger.error("CoquiTTS model was not initialized successfully. Cannot generate audio.")
            return 0.0, None

        processed_text = self._end_text(text)
        self._logger.debug(f"Sending text to Coqui TTS server: '{processed_text}'")

        try:
            req_params = {
                'text': processed_text,
                'speaker_id': self.speaker_id,
                'language_id': self.language_id,
            }
            if self.style_wav:
                req_params['style_wav'] = self.style_wav

            response = requests.get(
                f"{self.url}/api/tts",
                params=req_params,
                timeout=30 # 30秒のタイムアウトを設定
            )
            response.raise_for_status() # HTTPエラー (4xx, 5xx) が発生した場合に例外を発生させる

        except requests.exceptions.Timeout:
            self._logger.error(f"Coqui TTS server API call timed out after 30 seconds.")
            return 0.0, None
        except requests.exceptions.RequestException as e:
            self._logger.error(f"Coqui TTS server API call error: {e}\n{traceback.format_exc()}")
            return 0.0, None
        except Exception as e:
            self._logger.error(f"An unexpected error occurred during Coqui TTS API call: {e}\n{traceback.format_exc()}")
            return 0.0, None

        # レスポンスの検証
        if response.status_code == 200 and 'Content-Type' in response.headers and response.headers['Content-Type'] == 'audio/wav':
            audio_buffer = io.BytesIO(response.content)
            audio_buffer.seek(0) # バッファの読み取り位置を先頭に戻す

            try:
                # WAVファイルのヘッダを読み取り、再生時間を計算
                with wave.open(audio_buffer, 'r') as audio_file:
                    frame_rate = audio_file.getframerate()
                    n_frames = audio_file.getnframes()
                    if frame_rate > 0:
                        play_time = n_frames / float(frame_rate)
                    else:
                        play_time = 0.0
                        self._logger.warn("Coqui TTS: Received WAV has zero frame rate. Cannot calculate play time.")

                self._logger.info(f'Calculated Play Time[s] (Coqui TTS): {play_time:.4f}')
                return play_time, audio_buffer

            except wave.Error as e:
                self._logger.error(f"Coqui TTS: Error reading WAV header from response: {e}\n{traceback.format_exc()}")
                return 0.0, None
            except Exception as e:
                self._logger.error(f"Coqui TTS: An unexpected error occurred while processing audio buffer: {e}\n{traceback.format_exc()}")
                return 0.0, None

        else:
            self._logger.error(f"Coqui TTS: No valid audio received. Status: {response.status_code}, Content-Type: {response.headers.get('Content-Type')}, Response Text: {response.text[:200]}")
            return 0.0, None