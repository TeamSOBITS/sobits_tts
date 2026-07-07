from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    tts_name_arg = DeclareLaunchArgument(
        'tts_name',
        default_value='voicevox',
        description='TTS model to use (e.g., kokoro, parler).'
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

    voicevox_style_id_arg = DeclareLaunchArgument(
        'voicevox_style_id',
        default_value='14',
        description='Style ID for Voicevox TTS.'
    )

    voicevox_model_file_num_arg = DeclareLaunchArgument(
        'voicevox_model_file_num',
        default_value='1.vvm',
        description='Model file number for Voicevox TTS.'
    )

    voicevox_speed_scale_arg = DeclareLaunchArgument(
        'voicevox_speed_scale',
        default_value='1.0',
        description='Speech speed scale. 1.0 is normal, 1.5 speeds it up by 50%, under 1.0 slows it down.'
    )

    voicevox_pitch_scale_arg = DeclareLaunchArgument(
        'voicevox_pitch_scale',
        default_value='0.0',
        description='Speech pitch scale. Positive values make the voice higher (e.g., +1.0), negative values lower it (e.g., -1.0).'
    )

    voicevox_intonation_scale_arg = DeclareLaunchArgument(
        'voicevox_intonation_scale',
        default_value='1.0',
        description='Speech intonation. 1.0 is natural, lower values make it monotonous.'
    )

    voicevox_volume_scale_arg = DeclareLaunchArgument(
        'voicevox_volume_scale',
        default_value='1.0',
        description='Speech volume scale. 1.0 is normal, 2.0 doubles the volume, 0.5 reduces it by half.'
    )

    voicevox_pre_phoneme_length_arg = DeclareLaunchArgument(
        'voicevox_pre_phoneme_length',
        default_value='0.1',
        description='Silence duration before speech. Increasing this value adds silence before speech starts.'
    )

    voicevox_post_phoneme_length_arg = DeclareLaunchArgument(
        'voicevox_post_phoneme_length',
        default_value='0.1',
        description='Silence duration after speech. Increasing this value adds silence after speech ends.'
    )

    voicevox_output_sampling_rate_arg = DeclareLaunchArgument(
        'voicevox_output_sampling_rate',
        default_value='48000',
        description='Output sampling rate for speech. '
    )

    voicevox_output_stereo_arg = DeclareLaunchArgument(
        'voicevox_output_stereo',
        default_value='false',
        description='Whether to output stereo sound. False for mono, True for stereo sound field.'
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
            {'voicevox.style_id': ParameterValue(LaunchConfiguration('voicevox_style_id'), value_type=int)},
            {'voicevox.model_file_num': ParameterValue(LaunchConfiguration('voicevox_model_file_num'))},
            {'voicevox.speed_scale': ParameterValue(LaunchConfiguration('voicevox_speed_scale'), value_type=float)},
            {'voicevox.pitch_scale': ParameterValue(LaunchConfiguration('voicevox_pitch_scale'), value_type=float)},
            {'voicevox.intonation_scale': ParameterValue(LaunchConfiguration('voicevox_intonation_scale'), value_type=float)},
            {'voicevox.volume_scale': ParameterValue(LaunchConfiguration('voicevox_volume_scale'), value_type=float)},
            {'voicevox.pre_phoneme_length': ParameterValue(LaunchConfiguration('voicevox_pre_phoneme_length'), value_type=float)},
            {'voicevox.post_phoneme_length': ParameterValue(LaunchConfiguration('voicevox_post_phoneme_length'), value_type=float)},
            {'voicevox.output_sampling_rate': ParameterValue(LaunchConfiguration('voicevox_output_sampling_rate'), value_type=int)},
            {'voicevox.output_stereo': ParameterValue(LaunchConfiguration('voicevox_output_stereo'), value_type=bool)},
        ]
    )

    return LaunchDescription([
        tts_name_arg,
        speaker_volume_arg,
        playback_speed_arg,
        voicevox_style_id_arg,
        voicevox_model_file_num_arg,
        voicevox_speed_scale_arg,
        voicevox_pitch_scale_arg,
        voicevox_intonation_scale_arg,
        voicevox_volume_scale_arg,
        voicevox_pre_phoneme_length_arg,
        voicevox_post_phoneme_length_arg,
        voicevox_output_sampling_rate_arg,
        voicevox_output_stereo_arg,
        namespace_arg,                                
        tts_server_node
    ])
