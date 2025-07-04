import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.parameter_descriptions import ParameterValue 

def generate_launch_description():
    """
    Coqui TTSモデルを使用するためのLaunchDescriptionを生成します。
    tts_action_serverノードを起動し、Coqui TTS固有のパラメータを渡します。
    """

    # 使用するTTSモデル名をROSパラメータとして宣言
    # このLaunchファイルではCoqui TTSを使用するため、デフォルトを 'coqui' に設定
    tts_name_arg = DeclareLaunchArgument(
        'tts_name',
        default_value='coqui', # Coqui TTS モデルを指定
        description='Name of the TTS model to use (e.g., kokoro, openpico, parler, coqui).'
    )

    # --- Coqui TTS 固有のパラメータ ---
    # sobits_tts/include/coqui_tts.py で宣言されているパラメータと一致させる
    coqui_url_arg = DeclareLaunchArgument(
        'coqui_url',
        default_value='http://localhost:5002', # Coqui TTSサーバーのURL
        description='URL of the Coqui TTS server.'
    )

    coqui_add_stop_char_arg = DeclareLaunchArgument(
        'coqui_add_stop_char',
        default_value='True', # テキストの最後に句読点を自動追加するか
        description='Whether to add a stop character (., ;, !, ?) to the end of the text if missing.'
    )

    coqui_speaker_id_arg = DeclareLaunchArgument(
        'coqui_speaker_id',
        default_value='p225', # 使用するスピーカーID (Coqui TTSサーバーに依存)
        description='Speaker ID for Coqui TTS synthesis.'
    )

    coqui_language_id_arg = DeclareLaunchArgument(
        'coqui_language_id',
        default_value='', # 使用する言語ID (Coqui TTSサーバーに依存、空の場合はデフォルト)
        description='Language ID for Coqui TTS synthesis.'
    )

    coqui_style_wav_arg = DeclareLaunchArgument(
        'coqui_style_wav',
        default_value='', # スタイル転送用のWAVファイルパス (Coqui TTSサーバーから参照可能)
        description='Path to a WAV file for style transfer (e.g., voice cloning).'
    )

    tts_server_node = Node(
        package='sobits_tts',
        executable='tts_action_server', 
        name='tts_action_server',
        output='screen', 
        parameters=[
            {'tts_name': LaunchConfiguration('tts_name')},
            {'coqui.url': LaunchConfiguration('coqui_url')},
            {'coqui.add_stop_char': LaunchConfiguration('coqui_add_stop_char')},
            {'coqui.speaker_id': LaunchConfiguration('coqui_speaker_id')},
            {'coqui.language_id': LaunchConfiguration('coqui_language_id')},
            {'coqui.style_wav': LaunchConfiguration('coqui_style_wav')},
        ]
    )

    return LaunchDescription([
        tts_name_arg,
        coqui_url_arg,
        coqui_add_stop_char_arg,
        coqui_speaker_id_arg,
        coqui_language_id_arg,
        coqui_style_wav_arg,
        tts_server_node
    ])
