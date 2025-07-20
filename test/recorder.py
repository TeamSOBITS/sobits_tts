import re
import os
import subprocess
import logging
import threading
import time
import wave
import sys
from ament_index_python.packages import get_package_share_directory

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

try:
    SOBITS_INTERFACES_SHARE_DIR = get_package_share_directory('sobits_interfaces')
    soundfileS_PATH = os.path.join(SOBITS_INTERFACES_SHARE_DIR, 'mp3')
    if not os.path.isdir(soundfileS_PATH):
        raise FileNotFoundError(f"Sound files directory not found: {soundfileS_PATH}")
except Exception:
    logger.warning("Start and End sound files not found. Sound effects will be skipped.")
    soundfileS_PATH = None

PULSEAUDIO_SOURCE_NAME_PATTERN = re.compile(r'^\s*(?:Name|名前):\s*(.+)\s*$')
PULSEAUDIO_SAMPLE_SPEC_PATTERN = re.compile(r'^\s*(?:Sample Specification|サンプル仕様):\s*(\S+)\s+(\d+)ch\s+(\d+)Hz')

try:
    SPEECH_SOBITS_TTS_SHARE_DIR = get_package_share_directory('sobits_tts')
    AUDIO_OUTPUT_DIR = os.path.normpath(os.path.join(SPEECH_SOBITS_TTS_SHARE_DIR, '..', '..', '..', '..',
                                                'src', 'sobits_tts', 'soundfile'))
except Exception:
    logger.warning("Using current directory for audio output.")
    AUDIO_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test')

os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)
WAV_PATH = os.path.join(AUDIO_OUTPUT_DIR, 'record.wav')
print(f"Save location: {WAV_PATH}")

_audio_frames = []
_recording_active = False
_recording_process = None

def parse_pulseaudio_sample_rate_and_channels(lines):
    for line in lines:
        m = PULSEAUDIO_SAMPLE_SPEC_PATTERN.match(line)
        if m:
            return int(m.group(3)), int(m.group(2))
    return None, None

def get_pulseaudio_source_info():
    try:
        info = subprocess.run(['pactl', 'info'], capture_output=True, text=True, check=True)
        default_source = None
        for line in info.stdout.splitlines():
            if "Default Source:" in line or "デフォルトソース:" in line:
                default_source = line.split(':', 1)[1].strip()
                break
        if not default_source:
            logger.warning("Default PulseAudio source not found.")
            return None, None, None

        list_sources = subprocess.run(['pactl', 'list', 'sources'], capture_output=True, text=True, check=True)
        blocks = []
        current_block = []
        for line in list_sources.stdout.splitlines():
            if line.strip().startswith("Source #"):
                if current_block:
                    blocks.append(current_block)
                current_block = [line]
            else:
                current_block.append(line)
        if current_block:
            blocks.append(current_block)

        for block in blocks:
            for line in block:
                m = PULSEAUDIO_SOURCE_NAME_PATTERN.match(line)
                if m and m.group(1).strip() == default_source:
                    rate, channels = parse_pulseaudio_sample_rate_and_channels(block)
                    return default_source, rate, channels

        logger.warning(f"Could not find detailed info for source '{default_source}'.")
        return default_source, None, None

    except FileNotFoundError:
        logger.error("Error: 'pactl' command not found. Ensure PulseAudio is installed and in your PATH.")
        return None, None, None
    except Exception as e:
        logger.error(f"PulseAudio source info error: {e}")
        return None, None, None

def play_sound(filename):
    global soundfileS_PATH
    if soundfileS_PATH is None:
        logger.debug(f"Sound file path not set, skipping playback of '{filename}'.")
        return

    path = os.path.join(soundfileS_PATH, filename)
    if not os.path.exists(path):
        logger.warning(f"⚠️ Sound file not found: {path} - skipping playback.")
        return

    try:
        subprocess.run(['ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet', path],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        logger.warning(f"⚠️ ffplay not found. Please install FFmpeg (e.g., sudo apt install ffmpeg): {filename}")
        soundfileS_PATH = None
    except subprocess.CalledProcessError as e:
        logger.warning(f"⚠️ Failed to play sound (ffplay error code {e.returncode}): {filename}")
        logger.debug(f"ffplay stdout: {e.stdout.decode().strip()}")
        logger.debug(f"ffplay stderr: {e.stderr.decode().strip()}")
    except Exception as e:
        logger.warning(f"⚠️ An error occurred during sound playback: {e}")

def capture(source_name, sample_rate, channels, recording_duration_seconds):
    global _audio_frames, _recording_active, _recording_process
    _audio_frames = []
    _recording_active = True

    CHUNK_SIZE = 1024
    bytes_per_second = sample_rate * channels * 2
    total_bytes_to_record = int(bytes_per_second * recording_duration_seconds)

    logger.info(f"Starting recording for {recording_duration_seconds} seconds...")

    try:
        _recording_process = subprocess.Popen([
            'parec', '-d', source_name,
            '--format=s16le',
            '--channels', str(channels),
            '--rate', str(sample_rate),
            '--file-format=raw',
        ], stdout=subprocess.PIPE)

        bytes_read = 0
        start_time = time.time()
        last_update_time = time.time()
        progress_bar_length = 50

        while bytes_read < total_bytes_to_record and _recording_active:
            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time > (recording_duration_seconds + 1):
                break

            data = _recording_process.stdout.read(CHUNK_SIZE)
            if not data:
                break
            _audio_frames.append(data)
            bytes_read += len(data)

            if current_time - last_update_time >= 0.1:
                progress = min(1.0, elapsed_time / recording_duration_seconds)
                filled_length = int(progress_bar_length * progress)
                bar = '█' * filled_length + '-' * (progress_bar_length - filled_length)
                percentage = int(progress * 100)
                sys.stdout.write(f'\rRecording: [{bar}] {percentage}% ({elapsed_time:.1f}/{recording_duration_seconds:.1f}s)')
                sys.stdout.flush()
                last_update_time = current_time

            time.sleep(0.001)

    except Exception as e:
        logger.error(f"An error occurred during recording: {e}")
    finally:
        _recording_active = False
        if _recording_process and _recording_process.poll() is None:
            _recording_process.terminate()
            try:
                _recording_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                _recording_process.kill()
                logger.warning("parec process forcibly terminated.")
        sys.stdout.write('\r' + ' ' * (progress_bar_length + 30) + '\r')
        sys.stdout.flush()
        logger.info("Recording thread finished.")

if __name__ == '__main__':
    source_name, sample_rate, channels = get_pulseaudio_source_info()

    if source_name is None:
        logger.fatal("Failed to get default microphone. Exiting.")
        exit(1)

    if sample_rate is None or channels is None:
        sample_rate = 16000
        channels = 1
        logger.info("Failed to get sample rate or channel information. Using default values (16kHz / Mono).")

    logger.info(f"Microphone: {source_name}, Sample Rate: {sample_rate} Hz, Channels: {channels}")

    while True:
        try:
            recording_duration_str = input("Input seconds to record? (example: 5): ")
            recording_duration_seconds = float(recording_duration_str)
            if recording_duration_seconds <= 0:
                print("Please enter a number greater than 0.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number.")

    logger.info("Playing recording start sound.")
    start_sound_thread = threading.Thread(target=play_sound, args=('start_sound.mp3',), daemon=True)
    start_sound_thread.start()
    start_sound_thread.join()

    capture_thread = threading.Thread(target=capture,
                                      args=(source_name, sample_rate, channels, recording_duration_seconds),
                                      daemon=True)
    capture_thread.start()

    capture_thread.join(timeout=recording_duration_seconds + 5)

    if capture_thread.is_alive():
        logger.warning("Recording thread did not finish within the specified time. Attempting to force termination.")
        _recording_active = False
        if _recording_process and _recording_process.poll() is None:
            _recording_process.terminate()
            try:
                _recording_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                _recording_process.kill()
                logger.warning("parec process forcibly terminated again.")

    logger.info("Recording finished.")
    logger.info("Playing recording end sound.")
    end_sound_thread = threading.Thread(target=play_sound, args=('end_sound.mp3',), daemon=True)
    end_sound_thread.start()
    end_sound_thread.join()

    if _audio_frames:
        with wave.open(WAV_PATH, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(_audio_frames))
        logger.info(f"Recorded WAV file saved to: {WAV_PATH}")
    else:
        logger.warning("No audio data was recorded. WAV file will not be created.")
