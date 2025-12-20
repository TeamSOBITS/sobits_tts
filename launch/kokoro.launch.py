from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.parameter_descriptions import ParameterValue 

def generate_launch_description():
    tts_name_arg = DeclareLaunchArgument(
        'tts_name',
        default_value='kokoro',
        description='Name of the TTS model to use (e.g., kokoro, parler).'
    )

    kokoro_lang_code_arg = DeclareLaunchArgument(   # 'a': English (US), 'b': English (UK)
        'kokoro_lang_code',                         # 'j': Japanese
        default_value='a',                          # 'e': Spanish, 'f': French, 'h': Hindi
        description='Language code for Kokoro TTS.' # 'i': Italian, 'p': Brazilian Portuguese
    )                                               # 'z': Mandarin Chinese: pip3 install misaki[zh]

    kokoro_voice_arg = DeclareLaunchArgument(       # English (US): af_heart, English (UK): bf_isabella
        'kokoro_voice',                             # Japanese: jf_alpha
        default_value='af_heart',                   # Spanish: ef_dora, French: ff_siwis, Hindi: hf_alpha	
        description='Voice model for Kokoro TTS.'   # Italian: if_sara, Brazilian Portuguese: pf_dora
    )                                               # Mandarin Chinese: zf_xiaobei

    kokoro_speech_speed_arg = DeclareLaunchArgument(
        'kokoro_speech_speed',
        default_value='1.0',
        description='Speech speed for Kokoro TTS. 0.5 for half speed, 2.0 for double speed.'
    )

    kokoro_split_regex_arg = DeclareLaunchArgument(
        'kokoro_split_regex',
        default_value= r'[\n,.!?、。！？]+',
        description='Regular expression to split text'
    )

    kokoro_deveice_arg = DeclareLaunchArgument(
        'kokoro_device',
        default_value='',
        description='Device to use for Kokoro TTS (e.g., cpu or cuda).'
    )

    tts_server_node = Node(
        package='sobits_tts',
        executable='tts_action_server', 
        name='tts_action_server',
        output='screen', 
        parameters=[
            {'tts_name': LaunchConfiguration('tts_name')},
            {'kokoro.lang_code': LaunchConfiguration('kokoro_lang_code')},
            {'kokoro.voice': LaunchConfiguration('kokoro_voice')},
            {'kokoro.speech_speed': LaunchConfiguration('kokoro_speech_speed')},
            {'kokoro.split_regex': ParameterValue(LaunchConfiguration('kokoro_split_regex'), value_type=str)},
            {'kokoro.device': LaunchConfiguration('kokoro_device')},
        ]
    )

    return LaunchDescription([
        tts_name_arg,
        kokoro_lang_code_arg,
        kokoro_voice_arg,
        kokoro_speech_speed_arg,
        kokoro_split_regex_arg,
        kokoro_deveice_arg,
        tts_server_node
    ])