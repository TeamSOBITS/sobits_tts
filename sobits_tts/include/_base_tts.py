# sobits_tts/include/_base_tts.py
from abc import ABC, abstractmethod
from typing import Tuple
import io
from rclpy.node import Node # 型ヒントのためインポート

class BaseTTSModel(ABC):
    """
    すべてのTTSモデル固有クラスが継承すべき抽象基底クラス。
    これにより、共通のTTSアクションサーバーは、モデル固有のクラスが
    必要なメソッドを持っていることを保証できる。
    """
    def __init__(self, node: Node, sample_rate: int):
        """
        モデルを初期化するコンストラクタ。
        :param node: ROSノードインスタンス（ROSパラメータ宣言やロガー用）
        :param sample_rate: 音声のサンプルレート
        """
        self._node = node
        self._logger = node.get_logger()
        self._sample_rate = sample_rate
        self._logger.debug(f"BaseTTSModel initialized for node: {node.get_name()} with sample rate: {sample_rate}")

    @abstractmethod
    def generate_audio(self, text: str) -> Tuple[float, io.BytesIO]:
        """
        与えられたテキストから音声データを生成し、バイトストリームとして返す抽象メソッド。
        すべての継承クラスはこのメソッドを実装する必要があります。
        
        :param text: 音声に変換するテキスト
        :return: (推定再生時間[秒], 音声データを含むio.BytesIOオブジェクト) のタプル
                 音声生成に失敗した場合は (0.0, None) を返すことも可能ですが、
                 基本的にはモデル固有の例外を発生させるべきです。
        """
        pass