import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.parameter_descriptions import ParameterValue 
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    tts_name_arg = DeclareLaunchArgument(
        'tts_name',
        default_value='openpico', # モデル名を 'openpico' に設定
        description='Name of the TTS model to use (e.g., kokoro, openpico).'
    )

    # --- Open JTalk / Pico TTS 共通パラメータ ---
    openpico_language_arg = DeclareLaunchArgument(
        'openpico_language',
        default_value='en', # デフォルト言語 ('en' または 'ja')
        description='Default language for synthesis ("en" for Pico TTS, "ja" for Open JTalk).'
    )
    
    # --- Open JTalk 固有パラメータ ---
    openpico_voice_data_ja_arg = DeclareLaunchArgument(
        'openpico_voice_data_ja',
        # default_value='/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice',
        # その他の Open JTalk 音声データ例
        # default_value = os.path.join(get_package_share_directory("sobits_tts"), "install", "mei_angry.htsvoice"),
        # default_value = os.path.join(get_package_share_directory("sobits_tts"), "install", "mei_bashful.htsvoice"),
        # default_value = os.path.join(get_package_share_directory("sobits_tts"), "install", "mei_happy.htsvoice"),
        default_value = os.path.join(get_package_share_directory("sobits_tts"), "install", "mei_normal.htsvoice"),
        # default_value = os.path.join(get_package_share_directory("sobits_tts"), "install", "mei_sad.htsvoice"),
        
        description='Path to Open JTalk voice data (.htsvoice file).'
    )
    openpico_dic_path_ja_arg = DeclareLaunchArgument(
        'openpico_dic_path_ja',
        default_value='/var/lib/mecab/dic/open-jtalk/naist-jdic',
        description='Path to Open JTalk dictionary (MeCab dictionary).'
    )

    # --- 外部コマンドパス (システム依存) ---
    openpico_open_jtalk_cmd_arg = DeclareLaunchArgument(
        'openpico_open_jtalk_cmd',
        default_value='open_jtalk',
        description='Command name for Open JTalk executable (e.g., "open_jtalk" or "/usr/local/bin/open_jtalk").'
    )
    openpico_pico2wave_cmd_arg = DeclareLaunchArgument(
        'openpico_pico2wave_cmd',
        default_value='pico2wave',
        description='Command name for Pico2wave executable (e.g., "pico2wave" or "/usr/bin/pico2wave").'
    )

    tts_server_node = Node(
        package='sobits_tts',
        executable='tts_action_server', 
        name='tts_action_server',
        output='screen', 
        parameters=[
            {'tts_name': LaunchConfiguration('tts_name')},
            
            # OpenPicoTTSModel 固有のパラメータ
            {'openpico.language': LaunchConfiguration('openpico_language')},
            {'openpico.voice_data_ja': LaunchConfiguration('openpico_voice_data_ja')},
            {'openpico.dic_path_ja': LaunchConfiguration('openpico_dic_path_ja')},
            {'openpico.open_jtalk_cmd': LaunchConfiguration('openpico_open_jtalk_cmd')},
            {'openpico.pico2wave_cmd': LaunchConfiguration('openpico_pico2wave_cmd')},
        ]
    )

    return LaunchDescription([
        tts_name_arg,
        openpico_language_arg,
        openpico_voice_data_ja_arg,
        openpico_dic_path_ja_arg,
        openpico_open_jtalk_cmd_arg,
        openpico_pico2wave_cmd_arg,
        
        tts_server_node
    ])