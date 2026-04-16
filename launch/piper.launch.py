import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():   
    piper_model_arg = DeclareLaunchArgument(
        'piper_model', default_value='en_US-lessac-medium',
        description='Piper model name (e.g., en_US-amy-medium) or path.'
    )

    speaker_volume_arg = DeclareLaunchArgument(
        'speaker_volume',
        default_value='',
        description='Playback volume for the synthesized speech (e.g., 100%, 150%).'
    )

    piper_length_scale_arg = DeclareLaunchArgument(
        'piper_length_scale', default_value='1.0',
        description='Speaking speed scale.'
    )

    piper_noise_scale_arg = DeclareLaunchArgument(
        'piper_noise_scale', default_value='0.667',
        description='Noise scale (emotional variability).'
    )

    piper_noise_w_scale_arg = DeclareLaunchArgument(
        'piper_noise_w_scale', default_value='0.8',
        description='Phoneme width noise scale.'
    )

    piper_volume_arg = DeclareLaunchArgument(
        'piper_volume', default_value='1.0',
        description='Output audio volume.'
    )

    piper_speaker_id_arg = DeclareLaunchArgument(
        'piper_speaker_id', default_value='0',
        description='Speaker ID for multi-speaker models.'
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
            {
                'tts_name': 'piper',
                'speaker_volume': LaunchConfiguration('speaker_volume'),
                'piper.model_path': LaunchConfiguration('piper_model'),
                'piper.length_scale': LaunchConfiguration('piper_length_scale'),
                'piper.noise_scale': LaunchConfiguration('piper_noise_scale'),
                'piper.noise_w_scale': LaunchConfiguration('piper_noise_w_scale'),
                'piper.volume': LaunchConfiguration('piper_volume'),
                'piper.speaker_id': LaunchConfiguration('piper_speaker_id'),
            }
        ]
    )

    return LaunchDescription([
        piper_model_arg,
        speaker_volume_arg,
        piper_length_scale_arg,
        piper_noise_scale_arg,
        piper_noise_w_scale_arg,
        piper_volume_arg,
        piper_speaker_id_arg,
        namespace_arg,                
        tts_server_node
    ])