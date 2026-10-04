from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    tts_name_arg = DeclareLaunchArgument(
        'tts_name',
        default_value='irodori',
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

    irodori_ref_wav_arg = DeclareLaunchArgument(
        'irodori_ref_wav',
        default_value='',
        description='Reference voice wav (package://<pkg>/<path> is allowed). Empty for no reference.'
    )

    irodori_caption_arg = DeclareLaunchArgument(
        'irodori_caption',
        default_value='',
        description='Caption describing the voice and speaking style (Japanese).'
    )

    irodori_num_steps_arg = DeclareLaunchArgument(
        'irodori_num_steps',
        default_value='16',
        description='Sampling steps. Higher values improve quality but increase latency.'
    )

    irodori_seed_arg = DeclareLaunchArgument(
        'irodori_seed',
        default_value='0',
        description='Random seed. The same seed gives the same speech for the same text.'
    )

    irodori_checkpoint_arg = DeclareLaunchArgument(
        'irodori_checkpoint',
        default_value='Aratako/Irodori-TTS-v4.1-Small',
        description='Hugging Face checkpoint of Irodori TTS.'
    )

    irodori_device_arg = DeclareLaunchArgument(
        'irodori_device',
        default_value='cuda',
        description='Device to use (cuda or cpu).'
    )

    irodori_port_arg = DeclareLaunchArgument(
        'irodori_port',
        default_value='50070',
        description='Port of the Irodori API server (listens on 127.0.0.1 only).'
    )

    irodori_cache_dir_arg = DeclareLaunchArgument(
        'irodori_cache_dir',
        default_value='~/.sobits_tts/irodori/cache',
        description='Directory to cache generated speech.'
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
            {'irodori.ref_wav': ParameterValue(LaunchConfiguration('irodori_ref_wav'), value_type=str)},
            {'irodori.caption': ParameterValue(LaunchConfiguration('irodori_caption'), value_type=str)},
            {'irodori.num_steps': ParameterValue(LaunchConfiguration('irodori_num_steps'), value_type=int)},
            {'irodori.seed': ParameterValue(LaunchConfiguration('irodori_seed'), value_type=int)},
            {'irodori.checkpoint': ParameterValue(LaunchConfiguration('irodori_checkpoint'), value_type=str)},
            {'irodori.device': ParameterValue(LaunchConfiguration('irodori_device'), value_type=str)},
            {'irodori.port': ParameterValue(LaunchConfiguration('irodori_port'), value_type=int)},
            {'irodori.cache_dir': ParameterValue(LaunchConfiguration('irodori_cache_dir'), value_type=str)},
        ]
    )

    return LaunchDescription([
        tts_name_arg,
        speaker_volume_arg,
        playback_speed_arg,
        irodori_ref_wav_arg,
        irodori_caption_arg,
        irodori_num_steps_arg,
        irodori_seed_arg,
        irodori_checkpoint_arg,
        irodori_device_arg,
        irodori_port_arg,
        irodori_cache_dir_arg,
        namespace_arg,
        tts_server_node
    ])
