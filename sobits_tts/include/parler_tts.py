import rclpy
from rclpy.node import Node
# BaseTTSModelを継承
from sobits_tts.include._base_tts import BaseTTSModel

# ParlerTTS関連のライブラリ
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import numpy as np
import soundfile as sf
import torch
import io
from typing import Tuple # generate_audioの型ヒント用
import traceback # エラーログ用
import time # 初期化時間計測とPyTorchコンパイルログ用

# 日本語特有の処理（ルビ挿入など）に使用
from rubyinserter import add_ruby

class ParlerTTSModel(BaseTTSModel):
    """
    ParlerTTSを使用して音声合成を行うTTSモデルクラス。
    BaseTTSModelを継承。
    """
    def __init__(self, node: Node, sample_rate: int):
        # BaseTTSModelのコンストラクタを呼び出す
        super().__init__(node, sample_rate)

        # ParlerTTS 固有のROSパラメータをここで宣言・取得
        # パラメータ名にはモデル固有のプレフィックス 'parler_tts.' をつける
        self._node.declare_parameter('parler_tts.model_name', 'parler-tts/parler-tts-mini-v1')
        self._node.declare_parameter('parler_tts.description', 'Jenna delivers a slightly expressive and animated speech with a moderate speed and pitch. The recording is of very high quality, with the speaker voice sounding clear and very close up.')
        self._node.declare_parameter('parler_tts.device', 'auto') # 'cuda:0', 'cpu', 'auto'

        # 宣言したパラメータの値を取得
        self.model_name = self._node.get_parameter('parler_tts.model_name').get_parameter_value().string_value
        self.description = self._node.get_parameter('parler_tts.description').get_parameter_value().string_value
        device_param = self._node.get_parameter('parler_tts.device').get_parameter_value().string_value

        # 使用するデバイス（CPUまたはGPU）を設定
        if device_param == 'auto':
            self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device_param
        self._logger.info(f"Using device for ParlerTTS: {self.device}")

        # モデル、トークナイザーのインスタンス変数を初期化
        self.model = None
        self.tokenizer = None
        self.prompt_tokenizer = None
        self.description_tokenizer = None
        self._initialized_successfully = False # 初期化成功フラグ

        self._logger.info(f"Loading ParlerTTS model: {self.model_name}...")
        try:
            self.model = ParlerTTSForConditionalGeneration.from_pretrained(self.model_name).to(self.device)
            self._logger.info("ParlerTTS model loaded.")
        except Exception as e:
            # ここで例外を再発生させないようにする
            self._logger.fatal(f"Failed to load ParlerTTS model '{self.model_name}': {e}\n{traceback.format_exc()}")
            return # 初期化失敗で__init__を抜ける

        # PyTorchのコンパイル機能が利用可能かチェックし、利用可能ならモデルをコンパイル
        if hasattr(torch, 'compile'):
            compile_start_time = time.time()
            try:
                self.model = torch.compile(self.model, mode="reduce-overhead")
                compile_end_time = time.time()
                self._logger.info(f"ParlerTTS model compiled successfully in {compile_end_time - compile_start_time:.4f} seconds.")
            except Exception as e:
                self._logger.warn(f"Failed to compile the ParlerTTS model: {e}. Using uncompiled model.\n{traceback.format_exc()}")
        else:
            self._logger.info("torch.compile() not available for ParlerTTS. Using uncompiled model.")
            
        # 言語に応じたトークナイザーをロードし、descriptionをトークナイズ
        try:
            if "japanese" in self.model_name.lower(): # モデル名に"japanese"が含まれるかで判定
                self._logger.info(f"Loading Japanese tokenizers for: {self.model_name}")
                self.prompt_tokenizer = AutoTokenizer.from_pretrained(self.model_name, subfolder="prompt_tokenizer")
                self.description_tokenizer = AutoTokenizer.from_pretrained(self.model_name, subfolder="description_tokenizer")
                self.prompt_tokenizer.pad_token_id = self.model.config.pad_token_id
                self.description_tokenizer.pad_token_id = self.model.config.pad_token_id
                self._logger.info("Japanese tokenizers loaded.")
            else:
                self._logger.info(f"Loading English tokenizer for: {self.model_name}")
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.tokenizer.pad_token_id = self.model.config.pad_token_id
                self.prompt_tokenizer = self.tokenizer
                self.description_tokenizer = self.tokenizer
                self._logger.info("English tokenizer loaded.")
        except Exception as e:
            self._logger.fatal(f"Failed to load tokenizers for '{self.model_name}': {e}\n{traceback.format_exc()}")
            return # 初期化失敗で__init__を抜ける
            
        # description をトークナイズし、デバイスに配置
        try:
            self.inputs = self.description_tokenizer(self.description, return_tensors="pt").to(self.device)
            self._logger.info("Description tokenized successfully.")
        except Exception as e:
            self._logger.fatal(f"Failed to tokenize description: {e}\n{traceback.format_exc()}")
            return # 初期化失敗で__init__を抜ける
        
        self._logger.info(f"ParlerTTSModel initialized for model: {self.model_name}")
        self._initialized_successfully = True # 初期化成功

    def generate_audio(self, text: str) -> Tuple[float, io.BytesIO]:
        """
        BaseTTSModelの抽象メソッドを実装。
        ParlerTTSを呼び出し、音声データをio.BytesIOとして返す。
        """
        if not self._initialized_successfully:
            self._logger.error("ParlerTTS model was not initialized successfully. Cannot generate audio.")
            return 0.0, None

        # 処理対象のテキストを初期化
        processed_text = text
        
        # 日本語特有の前処理
        if "japanese" in self.model_name.lower():
            # ルビ挿入処理を適用
            processed_text = add_ruby(text)
            self._logger.debug(f"Japanese text processed with ruby: {processed_text}")

        # 言語に応じたプロンプトトークナイザーを選択
        prompt_tokenizer = self.prompt_tokenizer

        # 処理済みのテキストをトークナイズし、デバイスに配置 (プロンプトとして使用)
        try:
             prompt_inputs = prompt_tokenizer(processed_text, return_tensors="pt").to(self.device)
        except Exception as e:
             self._logger.error(f"Error tokenizing prompt text for ParlerTTS ({self.model_name}): {e}\n{traceback.format_exc()}")
             return 0.0, None

        # 推論モードで音声データを生成
        with torch.inference_mode():
            try:
                 generation = self.model.generate(
                     input_ids=self.inputs.input_ids, # DescriptionのトークンID
                     attention_mask=self.inputs.attention_mask, # Descriptionのアテンションマスク
                     prompt_input_ids=prompt_inputs.input_ids, # PromptのトークンID
                     prompt_attention_mask=prompt_inputs.attention_mask, # Promptのアテンションマスク
                 )
            except Exception as e:
                 self._logger.error(f"Error during ParlerTTS model generation ({self.model_name}): {e}\n{traceback.format_exc()}")
                 return 0.0, None

        # 生成されたテンソルの後処理
        audio_arr = generation.cpu().numpy().squeeze().astype(np.float32)
        sampling_rate = self.model.config.sampling_rate

        # 音声の再生時間を計算
        play_time = 0.0
        if sampling_rate > 0 and len(audio_arr) > 0:
            play_time = len(audio_arr) / float(sampling_rate)
            self._logger.info(f'Calculated Play Time[s] (ParlerTTS - {self.model_name}): {play_time:.4f}')
        else:
            self._logger.error(f"Invalid audio data or sampling rate for ParlerTTS ({self.model_name}). Audio length: {len(audio_arr)}, Sampling rate: {sampling_rate}")
            return 0.0, None

        # 音声データをバイナリバッファに書き込み（WAV形式）
        buffer = io.BytesIO()
        try:
            sf.write(buffer, audio_arr, sampling_rate, format='WAV')
            buffer.seek(0)
            return play_time, buffer
        except Exception as e:
            self._logger.error(f"Error writing ParlerTTS WAV to buffer ({self.model_name}): {e}\n{traceback.format_exc()}")
            return 0.0, None