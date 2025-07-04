import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.parameter_descriptions import ParameterValue 

def generate_launch_description():
    tts_name_arg = DeclareLaunchArgument(
        'tts_name',
        default_value='parler', # モデル名を 'parler_tts' に設定
        description='Name of the TTS model to use (e.g., kokoro, openpico, parler_tts).'
    )

    parler_tts_model_name_arg = DeclareLaunchArgument(
        'parler_tts_model_name',
        default_value='parler-tts/parler-tts-mini-v1', # デフォルトの英語モデル
        description='Hugging Face model ID for ParlerTTS'

        #英語モデル
            #ミニ           ：parler-tts/parler-tts-mini-v1
            #ミニジェニー   ：parler-tts/parler-mini-v1-jenny
            #感情指定可能   ：parler-tts/parler-tts-mini-expresso
            #CPU向けジェニー：parler-tts/parler-tiny-v1-jenny
        #日本語モデル
            #ミニ           ：2121-8/japanese-parler-tts-mini
    )

    parler_tts_description_arg = DeclareLaunchArgument(
        'parler_tts_description',
        default_value='Jenna delivers a slightly expressive and animated speech with a moderate speed and pitch. The recording is of very high quality, with the speaker voice sounding clear and very close up.',
        description='Textual description of the desired voice characteristics for ParlerTTS.'
    )

    parler_tts_device_arg = DeclareLaunchArgument(
        'parler_tts_device',
        default_value='auto', # 'cuda:0', 'cpu', 'auto'
        description='Device to use for ParlerTTS inference (e.g., "cuda:0", "cpu", "auto").'
    )

    tts_server_node = Node(
        package='sobits_tts',
        executable='tts_action_server', 
        name='tts_action_server',
        output='screen', 
        parameters=[
            {'tts_name': LaunchConfiguration('tts_name')},
            {'parler_tts.model_name': LaunchConfiguration('parler_tts_model_name')},
            {'parler_tts.description': LaunchConfiguration('parler_tts_description')},
            {'parler_tts.device': LaunchConfiguration('parler_tts_device')},
        ]
    )

    return LaunchDescription([
        tts_name_arg,
        parler_tts_model_name_arg,
        parler_tts_description_arg,
        parler_tts_device_arg,
        tts_server_node
    ])
















































# 2121-8/japanese-parler-tts-mini-bate