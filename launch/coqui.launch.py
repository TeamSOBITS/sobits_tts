import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.parameter_descriptions import ParameterValue 

def generate_launch_description():
    tts_name_arg = DeclareLaunchArgument(
        'tts_name',
        default_value='coqui',
        description='Name of the TTS model to use (e.g., kokoro, openpico, parler, coqui).'
    )

    speaker_volume_arg = DeclareLaunchArgument(
        'speaker_volume',
        default_value='100%',
        description='Playback volume for the synthesized speech (e.g., 100%, 150%).'
    )

    coqui_url_arg = DeclareLaunchArgument(
        'coqui_url',
        default_value='http://localhost:5002',
        description='URL of the Coqui TTS server.'
    )

    coqui_add_stop_char_arg = DeclareLaunchArgument(
        'coqui_add_stop_char',
        default_value='True', 
        description='Whether to add a stop character (., ;, !, ?) to the end of the text if missing.'
    )

    coqui_speaker_id_arg = DeclareLaunchArgument(
        'coqui_speaker_id',
        default_value='p225',
        description='Speaker ID for Coqui TTS synthesis.'
    )

    coqui_language_id_arg = DeclareLaunchArgument(
        'coqui_language_id',
        default_value='',
        description='Language ID for Coqui TTS synthesis.'
    )

    coqui_style_wav_arg = DeclareLaunchArgument(
        'coqui_style_wav',
        default_value='',
        description='Path to a WAV file for style transfer (e.g., voice cloning).'
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
            {'coqui.url': LaunchConfiguration('coqui_url')},
            {'coqui.add_stop_char': LaunchConfiguration('coqui_add_stop_char')},
            {'coqui.speaker_id': LaunchConfiguration('coqui_speaker_id')},
            {'coqui.language_id': LaunchConfiguration('coqui_language_id')},
            {'coqui.style_wav': LaunchConfiguration('coqui_style_wav')},
        ]
    )

    return LaunchDescription([
        tts_name_arg,
        speaker_volume_arg,
        coqui_url_arg,
        coqui_add_stop_char_arg,
        coqui_speaker_id_arg,
        coqui_language_id_arg,
        coqui_style_wav_arg,
        namespace_arg,        
        tts_server_node
    ])
