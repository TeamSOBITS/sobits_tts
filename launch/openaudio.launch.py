from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PythonExpression
import os

def generate_launch_description():   
    tts_name_arg = DeclareLaunchArgument(
        'tts_name',
        default_value='openaudio',
        description='Name of the TTS model to use.'
    )
    listen_address_arg = DeclareLaunchArgument(
        'listen_address',
        default_value='0.0.0.0:8080',
        description='Listen address for the OpenAudioTTS API server.'
    )
    use_half_precision_arg = DeclareLaunchArgument(
        'use_half_precision',
        default_value='True',
        description='Use half precision (FP16) for OpenAudioTTS model.'
    )
    device_arg = DeclareLaunchArgument(
        'device',
        default_value='cuda',
        description='Device to use for OpenAudioTTS (e.g., cuda, cpu).'
    )
    compile_model_arg = DeclareLaunchArgument(
        'compile_model',
        default_value='False',
        description='Enable model compilation (torch.compile) for OpenAudioTTS.'
    )
    max_text_length_arg = DeclareLaunchArgument(
        'max_text_length',
        default_value='256',
        description='Maximum text length for OpenAudioTTS.'
    )

    chunk_length_arg = DeclareLaunchArgument(
        'chunk_length',
        default_value='200', 
        description='Chunk length for OpenAudioTTS inference.'
    )
    reference_audio_path_arg = DeclareLaunchArgument(
        'reference_audio_path',
        default_value='', 
        description='Path to the reference audio file for OpenAudioTTS.'
    )
    reference_text_arg = DeclareLaunchArgument(
        'reference_text',
        default_value="", 
        description='Reference text for OpenAudioTTS (if using reference audio).'
    )

    reference_id_arg = DeclareLaunchArgument(
        'reference_id',
        default_value='None',
        description='Reference ID for OpenAudioTTS.'
    )
    seed_arg = DeclareLaunchArgument(
        'seed',
        default_value='None',
        description='Seed for OpenAudioTTS generation.'
    )
    use_memory_cache_arg = DeclareLaunchArgument(
        'use_memory_cache',
        default_value='True',
        description='Use memory cache for OpenAudioTTS. ("on" or "off")'
    )
    normalize_arg = DeclareLaunchArgument(
        'normalize',
        default_value='True',
        description='Normalize output audio for OpenAudioTTS.'
    )
    max_new_tokens_arg = DeclareLaunchArgument(
        'max_new_tokens',
        default_value='1024',
        description='Max new tokens for OpenAudioTTS.'
    )
    top_p_arg = DeclareLaunchArgument(
        'top_p',
        default_value='0.8',
        description='Top-p sampling parameter for OpenAudioTTS.'
    )
    repetition_penalty_arg = DeclareLaunchArgument(
        'repetition_penalty',
        default_value='1.1',
        description='Repetition penalty for OpenAudioTTS.'
    )
    temperature_arg = DeclareLaunchArgument(
        'temperature',
        default_value='0.8',
        description='Temperature for OpenAudioTTS.'
    )

    from launch_ros.descriptions import ParameterValue

    tts_server_node = Node(
        package='sobits_tts',
        executable='tts_action_server',
        name='tts_action_server',
        output='screen',
        parameters=[
            {'tts_name': LaunchConfiguration('tts_name')},

            {'openaudio_tts.listen_address': LaunchConfiguration('listen_address')},
            {'openaudio_tts.use_half_precision': ParameterValue(LaunchConfiguration('use_half_precision'), value_type=bool)},
            {'openaudio_tts.device': LaunchConfiguration('device')},
            {'openaudio_tts.compile_model': ParameterValue(LaunchConfiguration('compile_model'), value_type=bool)},
            {'openaudio_tts.max_text_length': ParameterValue(LaunchConfiguration('max_text_length'), value_type=int)},

            {'openaudio_tts.chunk_length': ParameterValue(LaunchConfiguration('chunk_length'), value_type=int)},
            {'openaudio_tts.reference_audio_path': LaunchConfiguration('reference_audio_path')},
            {'openaudio_tts.reference_text': LaunchConfiguration('reference_text')},
            {'openaudio_tts.reference_id': LaunchConfiguration('reference_id')},
            {'openaudio_tts.seed': LaunchConfiguration('seed')},

            {'openaudio_tts.use_memory_cache': ParameterValue(LaunchConfiguration('use_memory_cache'), value_type=bool)},
            {'openaudio_tts.normalize': ParameterValue(LaunchConfiguration('normalize'), value_type=bool)},
            {'openaudio_tts.max_new_tokens': ParameterValue(LaunchConfiguration('max_new_tokens'), value_type=int)},
            {'openaudio_tts.top_p': ParameterValue(LaunchConfiguration('top_p'), value_type=float)},
            {'openaudio_tts.repetition_penalty': ParameterValue(LaunchConfiguration('repetition_penalty'), value_type=float)},
            {'openaudio_tts.temperature': ParameterValue(LaunchConfiguration('temperature'), value_type=float)},
        ]
    )
    return LaunchDescription([
        tts_name_arg,
        listen_address_arg,
        use_half_precision_arg,
        device_arg,
        compile_model_arg,
        max_text_length_arg,
        chunk_length_arg,
        reference_audio_path_arg,
        reference_text_arg,
        reference_id_arg,
        seed_arg,
        use_memory_cache_arg,
        normalize_arg,
        max_new_tokens_arg,
        top_p_arg,
        repetition_penalty_arg,
        temperature_arg,
        
        tts_server_node
    ])