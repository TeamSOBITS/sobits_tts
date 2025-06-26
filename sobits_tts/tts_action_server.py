import rclpy
from rclpy.node import Node
import pygame
import time
import importlib
import io
import traceback

from sobits_interfaces.action import TextToSpeech
from rclpy.action import ActionServer, GoalResponse, CancelResponse

# TTSモデルインターフェースのインポート
from sobits_tts.include._base_tts import BaseTTSModel

class TTSActionServer(Node):
    def __init__(self):
        super().__init__('tts_action_server')

        # 使用するTTSモデル名をROSパラメータとして宣言
        self.declare_parameter('tts_model_name', 'kokoro') # デフォルトは'kokoro'

        self.tts_model_name = self.get_parameter('tts_model_name').get_parameter_value().string_value
        self.get_logger().info(f"Selected TTS model: {self.tts_model_name}")

        self.sample_rate = 24000 # 共通のサンプルレート（必要に応じてパラメータ化）

        self._tts_model_instance = None
        self._mixer_initialized = False

        # 1. モデル固有モジュールのロードと初期化
        try:
            module_path = f'sobits_tts.include.{self.tts_model_name}_tts'
            tts_model_module = importlib.import_module(module_path)
            
            # モジュール内のモデルクラスを取得し、インスタンス化
            # クラス名は 'KokoroTTSModel' のように、モジュール名から推測できるようにする
            # 例: kokoro_tts.py に KokoroTTSModel クラスがある場合
            model_class_name = f"{self.tts_model_name.capitalize()}TTSModel"
            ModelClass = getattr(tts_model_module, model_class_name)
            
            # モデルインスタンスを生成し、ROSノードと共通のサンプルレートを渡す
            if not issubclass(ModelClass, BaseTTSModel):
                raise TypeError(f"Model class {model_class_name} does not inherit from BaseTTSModel. Please check its definition.")

            self._tts_model_instance = ModelClass(node=self, sample_rate=self.sample_rate)
            self.get_logger().info(f"Successfully loaded and initialized TTS model '{self.tts_model_name}'.")

        except ModuleNotFoundError:
            self.get_logger().fatal(f"TTS model module '{self.tts_model_name}_tts' not found in 'sobits_tts.include'. Please check spelling or installation of the model-specific file.")
            raise RuntimeError(f"TTS model '{self.tts_model_name}' not available. Module not found.")
        except AttributeError:
            self.get_logger().fatal(f"Model class '{model_class_name}' not found in '{module_path}'. Ensure the class name matches the expected format (e.g., 'KokoroTTSModel' for 'kokoro_tts').")
            raise RuntimeError(f"Model class not found for '{self.tts_model_name}'.")
        except TypeError as e:
            self.get_logger().fatal(f"Type error during model initialization for '{self.tts_model_name}': {e}")
            self.get_logger().fatal(traceback.format_exc()) 
            raise RuntimeError(f"Model initialization failed for '{self.tts_model_name}'.")
        except Exception as e:
            self.get_logger().fatal(f"An unexpected error occurred during TTS model loading/initialization for '{self.tts_model_name}': {e}") # exc_info=True を削除
            self.get_logger().fatal(traceback.format_exc()) 
            raise RuntimeError(f"Failed to load or initialize TTS model '{self.tts_model_name}'.")
        
        # 2. Pygameミキサーの初期化 (共通部分)
        try:
            pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=1, buffer=512)
            self.get_logger().info("Pygame mixer initialized.")
            self._mixer_initialized = True
        except Exception as e:
            self.get_logger().error(f"Failed to initialize Pygame mixer: {e}. Audio playback may not work.")
            self._mixer_initialized = False

        # 3. アクションサーバーの作成 (共通部分)
        self._action_server = ActionServer(
            self,
            TextToSpeech,
            'speech_word',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback)

        self.get_logger().info(f"TTS Action Server ready with model: {self.tts_model_name}")

    def destroy_node(self):
        self.get_logger().info('Shutting down TTS action server...')
        if pygame.mixer.get_init():
            try:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
                self.get_logger().info('Pygame mixer quit.')
            except Exception as e:
                 self.get_logger().error(f"Error quitting Pygame mixer: {e}")
        super().destroy_node()

    def goal_callback(self, goal_request):
        self.get_logger().debug(f"Received goal request with text: '{goal_request.text}'")
        # PygameとTTSモデルの両方が初期化されているか確認
        if not self._mixer_initialized or self._tts_model_instance is None:
            self.get_logger().error("Mixer or TTS model not initialized. Rejecting goal.")
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().debug('Received cancel request.')
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        feedback = TextToSpeech.Feedback()
        response = TextToSpeech.Result()
        text = goal_handle.request.text

        # 入力テキストのバリデーション
        if not isinstance(text, str) or not text.strip():
            self.get_logger().error(f"Input text is empty, blank, or not a string. Received: '{text}'")
            response.success = False
            goal_handle.abort()
            return response

        self.get_logger().info(f"Processing text: [{text}] using {self.tts_model_name} model.")

        # 再度、PygameとTTSモデルの初期化状態を確認
        if not pygame.mixer.get_init() or self._tts_model_instance is None:
            self.get_logger().error("Pygame mixer or TTS model is not initialized. Cannot play audio.")
            response.success = False
            goal_handle.abort()
            return response

        response.success = False # デフォルトは失敗
        play_time = 0.0
        audio_buffer = None

        try:
            # TTSモデル固有のインスタンスの音声生成関数を呼び出す
            # 返り値は推定再生時間とBytesIOオブジェクト
            play_time, audio_buffer = self._tts_model_instance.generate_audio(text)

            if audio_buffer is None or play_time <= 0:
                self.get_logger().error(f"Audio buffer generation failed or invalid play time ({play_time:.2f}s) from '{self.tts_model_name}' model. Check model logs for details.")
                response.success = False
                goal_handle.abort()
                return response

            # 共通の音声再生ロジック
            pygame.mixer.music.load(audio_buffer)
            pygame.mixer.music.play()

            start_playback_loop_time = time.time()
            feedback.remaining_time = play_time

            # 音声再生中のループ
            while pygame.mixer.music.get_busy():
                # キャンセルリクエストのチェック
                if goal_handle.is_cancel_requested:
                    self.get_logger().info('Goal canceled during playback.')
                    pygame.mixer.music.stop() # 音声停止
                    goal_handle.canceled() # ゴールをキャンセル状態に
                    response.success = False # キャンセルは成功ではない
                    return response # ここで処理を終了

                current_time_in_loop = time.time()
                elapsed_in_loop = current_time_in_loop - start_playback_loop_time
                response.total_time = elapsed_in_loop
                feedback.remaining_time = play_time - elapsed_in_loop

                if feedback.remaining_time < 0:
                    feedback.remaining_time = 0.0
                
                goal_handle.publish_feedback(feedback) # フィードバックを公開

                time.sleep(0.05) # 50ミリ秒ごとに更新

            # ループ終了後の処理（再生完了または予期せぬ停止）
            final_elapsed_time = time.time() - start_playback_loop_time
            response.total_time = final_elapsed_time
            
            # 再生完了の判断ロジック
            if abs(play_time - final_elapsed_time) < 0.5 or final_elapsed_time >= play_time:
                 self.get_logger().info(f"Playback completed. Estimated: {play_time:.2f}s, Actual: {final_elapsed_time:.2f}s")
                 response.success = True
                 goal_handle.succeed() # ゴールを成功状態に設定
            else:
                 self.get_logger().warn(f"Playback ended prematurely or unexpectedly. Estimated: {play_time:.2f}s, Actual: {final_elapsed_time:.2f}s")
                 response.success = False
                 goal_handle.abort() # ゴールを中断

            # 最後のフィードバック（残り時間0）
            feedback.remaining_time = 0.0
            goal_handle.publish_feedback(feedback)

        # エラーハンドリング
        except pygame.error as e:
            self.get_logger().error(f"Pygame error during audio playback: {e}")
            self.get_logger().error(traceback.format_exc()) # tracebackを別途出力
            response.success = False
            goal_handle.abort()
        except Exception as e:
            self.get_logger().error(f"An unexpected error occurred during audio generation or playback by TTS model: {e}") # exc_info=True を削除
            self.get_logger().error(traceback.format_exc()) # tracebackを別途出力
            response.success = False
            goal_handle.abort()
        
        return response

def main(args=None):
    rclpy.init(args=args)
    action_server = None
    try:
        action_server = TTSActionServer()
        rclpy.spin(action_server)
    except RuntimeError as e:
        # モデルロードやPygame初期化に失敗した場合の致命的なエラーハンドリング
        if action_server and rclpy.ok(): 
            action_server.get_logger().fatal(f"TTS Action Server could not be started due to initialization failure: {e}") 
            action_server.get_logger().fatal(traceback.format_exc()) # tracebackを別途出力
        else:
            try:
                temp_node = rclpy.create_node('tts_server_fatal_logger')
                temp_node.get_logger().fatal(f"Failed to initialize TTS Action Server: {e}") 
                temp_node.get_logger().fatal(traceback.format_exc()) # tracebackを別途出力
                temp_node.destroy_node()
            except Exception as log_e:
                print(f"FATAL ERROR: Could not initialize logger or TTS Action Server: {e}, Logger error: {log_e}")
    except KeyboardInterrupt:
        # Ctrl+Cによる正常終了を捕捉
        pass 
    except Exception as e:
        # その他の予期せぬエラー
        if action_server and rclpy.ok():
            action_server.get_logger().fatal(f"An unexpected error occurred in main loop: {e}") # exc_info=True を削除
            action_server.get_logger().fatal(traceback.format_exc()) # tracebackを別途出力
        else:
            try:
                temp_node = rclpy.create_node('tts_server_fatal_logger')
                temp_node.get_logger().fatal(f"An unexpected error occurred before node creation: {e}")
                temp_node.get_logger().fatal(traceback.format_exc()) # tracebackを別途出力
                temp_node.destroy_node()
            except Exception as log_e:
                print(f"FATAL ERROR: Could not initialize logger or TTS Action Server: {e}, Logger error: {log_e}")
    finally:
        # ROS 2がまだ実行中の場合、適切にシャットダウン
        if rclpy.ok():
            if action_server:
                action_server.destroy_node()
            rclpy.shutdown()

if __name__ == "__main__":
    main()