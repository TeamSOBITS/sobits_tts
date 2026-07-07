from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    tts_name_arg = DeclareLaunchArgument(
        'tts_name',
        default_value='supertonic',
        description='Name of the TTS model to use.'
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

    supertonic_device_arg = DeclareLaunchArgument(
        'supertonic_device',
        default_value='cpu',
        description='Device to use (e.g., cpu or cuda). Empty for auto-detection.'
    )

    supertonic_voice_name_arg = DeclareLaunchArgument(
        'supertonic_voice_name',
        default_value='F3',
        description='Voice name for Supertonic (e.g., F1, F2, M1, M2).'
    )

    supertonic_language_arg = DeclareLaunchArgument(
        'supertonic_language',
        default_value='en',
        description='Language code for synthesis (e.g., en, ko, es, fr, pt).'
    )

    supertonic_total_steps_arg = DeclareLaunchArgument(
        'supertonic_total_steps',
        default_value='8',
        description='Diffusion steps. Higher values improve quality but increase latency.'
    )

    supertonic_speed_arg = DeclareLaunchArgument(
        'supertonic_speed',
        default_value='1.05',
        description='Speech speed. 1.0 is normal speed.'
    )

    supertonic_max_chunk_length_arg = DeclareLaunchArgument(
        'supertonic_max_chunk_length',
        default_value='300',
        description='Maximum character length per chunk for synthesis.'
    )

    supertonic_silence_duration_arg = DeclareLaunchArgument(
        'supertonic_silence_duration',
        default_value='0.3',
        description='Silence duration between chunks in seconds.'
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
            {'playback_speed': ParameterValue(LaunchConfiguration('playback_speed'), value_type=float)},
            {'supertonic.device': LaunchConfiguration('supertonic_device')},
            {'supertonic.voice_name': LaunchConfiguration('supertonic_voice_name')},
            {'supertonic.language': LaunchConfiguration('supertonic_language')}, 
            {'supertonic.total_steps': LaunchConfiguration('supertonic_total_steps')},
            {'supertonic.speed': LaunchConfiguration('supertonic_speed')},
            {'supertonic.max_chunk_length': LaunchConfiguration('supertonic_max_chunk_length')},
            {'supertonic.silence_duration': LaunchConfiguration('supertonic_silence_duration')},
        ]
    )

    return LaunchDescription([
        tts_name_arg,
        speaker_volume_arg,
        playback_speed_arg,
        supertonic_device_arg,
        supertonic_voice_name_arg,
        supertonic_language_arg, 
        supertonic_total_steps_arg,
        supertonic_speed_arg,
        supertonic_max_chunk_length_arg,
        supertonic_silence_duration_arg,
        namespace_arg,                        
        tts_server_node
    ])