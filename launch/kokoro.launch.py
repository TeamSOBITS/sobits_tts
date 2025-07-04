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

    kokoro_lang_code_arg = DeclareLaunchArgument(
        'kokoro_lang_code',
        default_value='a',
        description='Language code for Kokoro TTS.'
    )

    # 🇺🇸 'a' => アメリカ英語, 🇬🇧 'b' => イギリス英語
    # 🇯🇵 'j' => 日本語
    # 🇪🇸 'e' => スペイン語
    # 🇫🇷 'f' => フランス語
    # 🇮🇳 'h' => ヒンディー語
    # 🇮🇹 'i' => イタリア語
    # 🇧🇷 'p' => ブラジルのポルトガル語
    # 🇨🇳 'z' => 中国語(普通話): pip3 install misaki[zh]

    kokoro_voice_arg = DeclareLaunchArgument(
        'kokoro_voice',
        default_value='af_heart',
        description='Voice model for Kokoro TTS.'
    )

    # 🇺🇸 アメリカ英語：af_heart
    # 🇬🇧 イギリス英語：bf_isabella
    # 🇯🇵 日本語      ：jf_alpha
    # 🇪🇸 スペイン語  ：ef_dora
    # 🇫🇷 フランス語  ：ff_siwis
    # 🇮🇳 ヒンディー語：hf_alpha	
    # 🇮🇹 イタリア語  ：if_sara
    # 🇧🇷 ブラジルのポルトガル語：pf_dora
    # 🇨🇳 中国語(普通話)：zf_xiaobei

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
        ]
    )

    return LaunchDescription([
        tts_name_arg,
        kokoro_lang_code_arg,
        kokoro_voice_arg,
        kokoro_speech_speed_arg,
        kokoro_split_regex_arg,
        
        tts_server_node
    ])