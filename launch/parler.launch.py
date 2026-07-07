import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.parameter_descriptions import ParameterValue 

def generate_launch_description():
    tts_name_arg = DeclareLaunchArgument(
        'tts_name',
        default_value='parler',
        description='Name of the TTS model to use (e.g., kokoro, openpico, parler_tts).'
    )

    speaker_volume_arg = DeclareLaunchArgument(
        'speaker_volume',
        default_value='',
        description='Playback volume for the synthesized speech (e.g., 100%, 150%).'
    )

    playback_speed_arg = DeclareLaunchArgument(
        'playback_speed',
        default_value='1.0',
        description='Post-generation playback speed multiplier (0.5-2.0). Pitch is preserved.'
    )

    parler_tts_model_name_arg = DeclareLaunchArgument(
        'parler_tts_model_name',
        default_value='parler-tts/parler-tts-mini-v1', 
        description='Hugging Face model ID for ParlerTTS'
    )

    parler_tts_description_arg = DeclareLaunchArgument(
        'parler_tts_description',
        default_value='Jenna delivers a slightly expressive and animated speech with a moderate speed and pitch. The recording is of very high quality, with the speaker voice sounding clear and very close up.',
        description='Textual description of the desired voice characteristics for ParlerTTS.'
    )

    parler_tts_device_arg = DeclareLaunchArgument(
        'parler_tts_device',
        default_value='auto',
        description='Device to use for ParlerTTS inference (e.g., "cuda:0", "cpu", "auto").'
    )
    namespace_arg = DeclareLaunchArgument(
        "namespace",
        default_value="",
        description="Namespace for the nodes"
    )    

    tts_server_node = Node(
        package='sobits_tts',
        executable='tts_action_server', 
        name='tts_action_server',
        namespace=LaunchConfiguration('namespace'),                        
        output='screen', 
        parameters=[
            {'tts_name': LaunchConfiguration('tts_name')},
            {'speaker_volume': LaunchConfiguration('speaker_volume')},
            {'playback_speed': LaunchConfiguration('playback_speed')},
            {'parler_tts.model_name': LaunchConfiguration('parler_tts_model_name')},
            {'parler_tts.description': LaunchConfiguration('parler_tts_description')},
            {'parler_tts.device': LaunchConfiguration('parler_tts_device')},
        ]
    )

    return LaunchDescription([
        tts_name_arg,
        speaker_volume_arg,
        playback_speed_arg,
        parler_tts_model_name_arg,
        parler_tts_description_arg,
        parler_tts_device_arg,
        namespace_arg,        
        tts_server_node
    ])
















































# 2121-8/japanese-parler-tts-mini-bate