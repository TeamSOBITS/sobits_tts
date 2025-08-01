<a name="readme-top"></a>

[JA](README_detail.md) | [EN](README_detail.en.md)

[Back](README.en.md)

-----

<details>
<summary>Table of Contents</summary>
<ol>
<li><a href="#kokoro-tts">Kokoro TTS</a></li>
<li><a href="#openpico">OpenPico (formerly Text_to_Speech)</a></li>
<li><a href="#coqui-tts">Coqui TTS</a></li>
<li><a href="#parler-tts">Parler TTS</a></li>
<li><a href="#open-audio-tts">Open Audio TTS</a></li>
<li><a href="#voicevox-tts">Voicevox TTS</a></li>
</ol>
</details>

# Kokoro TTS

[Kokoro](https://huggingface.co/hexgrad/Kokoro-82M) is an open-weight Text-to-Speech (TTS) model with 82 million parameters.
Despite its lightweight architecture, it achieves quality comparable to larger models while significantly improving processing speed and cost efficiency.

## Installation

1.  Navigate to the `sobits_tts` install directory.

    ```sh
    cd ~/colcon_ws/src/sobits_tts/install/
    ```

2.  Install the model.

    ```bash
    bash kokoro.sh
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

-----

## Launch and Usage

1.  Launch `kokoro.launch.py`.

    ```bash
    ros2 launch sobits_tts kokoro.launch.py
    ```

2.  Start the Action Client.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

-----

## Parameters

### Supported Languages

Kokoro TTS supports the following languages.
Change **kokoro_lang_code** in [kokoro.launch.py](launch/kokoro.launch.py) to your desired language.

| Supported Language | lang_code |
| ----- | ----- |
| American English | a |
| British English | b |
| Japanese | j |
| Spanish | e |
| French | f |
| Hindi | h |
| Italian | i |
| Brazilian Portuguese | p |
| Mandarin Chinese | z |

  * When using Chinese, execute the following command:
    ```sh
    pip3 install misaki[zh]==0.9.4
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Speaker

Kokoro TTS supports various speakers for each language.
Change **kokoro_voice** in [kokoro.launch.py](launch/kokoro.launch.py) to your desired speaker.
Here are a few examples:

  - American English
      - Female
          - af_heart
          - af_bella
      - Male
          - am_fenrir
          - am_puck
  - Japanese
      - Female
          - jf_alpha
      - Male
          - jm_kumo

More speakers are available for American English, Japanese, and other languages.
For more details, refer to [this link](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md).

> You can also make Japanese sound like it's spoken by a foreigner. To do so, set the following:
>
>   - Language (`lang_code`): Japanese
>   - Speaker (`voice`): English speaker
>   - Text to be spoken: Japanese

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Speech Speed

To change the speech speed, modify **kokoro\_speech\_speed** in [kokoro.launch.py](https://www.google.com/search?q=launch/kokoro.launch.py) (default value: `1.0`).
 
Example: To set to 1.2x speed

```sh
kokoro_speech_speed_arg = DeclareLaunchArgument(
    'kokoro_speech_speed',
    default_value='1.2',
    description='Speech speed for Kokoro TTS. 0.5 for half speed, 2.0 for double speed.'
)
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Delimiter Characters

To split speech at specific characters, modify **kokoro\_split\_regex** in [kokoro.launch.py](https://www.google.com/search?q=launch/kokoro.launch.py) (default value: `r'[\n,.!?、。！？]+'`).
 
Example: To split at `*`

```sh
kokoro_split_regex_arg = DeclareLaunchArgument(
    'kokoro_split_regex',
    default_value= r'[\n,.!?、。！？]+',
    description='Regular expression to split text'
)
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

-----

# OpenPico

OpenPico combines [OpenJTalk](https://open-jtalk.sourceforge.net/) and [SVOX Pico](https://www.openhab.org/addons/voice/picotts/).
OpenJTalk is open-source speech synthesis software for converting Japanese text to audio.
SVOX Pico is a lightweight Text-to-Speech (TTS) engine that supports various languages.

## Installation

1.  Navigate to the `sobits_tts` install directory.

    ```sh
    cd ~/colcon_ws/src/sobits_tts/install/
    ```

2.  Install the model.

    ```bash
    bash openpico.sh
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

-----

## Launch and Usage

1.  Launch `openpico.launch.py`.

    ```bash
    ros2 launch sobits_tts openpico.launch.py
    ```

2.  Start the Action Client.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

-----

## Parameters

### Supported Languages

OpenPico supports the following languages.
Change **openpico_language** in [openpico.launch.py](launch/openpico.launch.py) to your desired language.

| Supported Language | openpico\_language |
| ----- | ----- |
| English | en |
| Japanese | ja |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Speaker

OpenPico supports various speakers only for Japanese.
Change **openpico_voice_data_ja** in [openpico.launch.py](launch/openpico.launch.py) to the file path of your desired speaker.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

-----

# Coqui TTS

[Coqui TTS](https://github.com/coqui-ai/TTS) is an open-source speech synthesis toolkit for generating speech from text.

## Installation

1.  Navigate to the `sobits_tts` install directory.
    ```sh
    cd ~/colcon_ws/src/sobits_tts/install/
    ```
2.  Install the model.
    ```bash
    bash coqui.sh
    ```
3.  Create an `alias` to easily run the TTS server.
      - For **CPU only**:
    <!-- end list -->
    ```sh
    $ echo "alias tts_launch='docker run --rm -it -p 5002:5002 -v ~/{PATH_ROS_WS_LOCAL}/src/coqui_tts_ros/models/:/root/.local/share/tts/ --entrypoint \"tts-server\" ghcr.io/coqui-ai/tts-cpu'" >> ~/.bash_alias
    ```
      - For **GPU**:
    <!-- end list -->
    ```sh
    $ echo "alias tts_launch='docker run --rm -it -p 5002:5002 --gpus all -v ~/{PATH_ROS_WS_LOCAL}/src/coqui_tts_ros/models/:/root/.local/share/tts/ --entrypoint \"tts-server\" ghcr.io/coqui-ai/tts'" >> ~/.bash_alias
    ```

> [!IMPORTANT]
> `{PATH_ROS_WS_LOCAL}` is the **local path** to your ROS workspace.

> [!IMPORTANT]
> If you are already inside a Docker container, you need to run command 6 on your local machine.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Launch and Usage

1.  Start the TTS server on your **local machine**.

      - For **CPU only**:

    <!-- end list -->

    ```sh
    $ tts_launch --model_name tts_models/en/vctk/vits
    ```

      - For **GPU**:

    <!-- end list -->

    ```sh
    $ tts_launch --model_name tts_models/en/vctk/vits --use_cuda true
    ```

2.  Launch `coqui.launch.py`.

    ```bash
    ros2 launch sobits_tts coqui.launch.py
    ```

3.  Start the Action Client.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

-----

## Parameters

You can specify the following parameters in [coqui.launch.py](https://www.google.com/search?q=launch/coqui.launch.py).

| Parameter | Parameter Name | Description | Default Value |
| ----- | ----- | ----- | ----- |
| Supported Language | `coqui_language_id` | ID of the language to use (English only) | |
| Speaker | `coqui_speaker_id` | ID of the speaker to use (p225 \~ p376) | p225 |
| Auto Punctuation | `coqui_add_stop_char` | Whether to automatically add punctuation at the end of the text | True |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

# Parler TTS

Parler TTS is a lightweight Text-to-Speech (TTS) model capable of generating high-quality, natural-sounding audio in the style of a specific speaker (gender, pitch, speaking manner, etc.).

It is replicated from the paper [Natural language guidance of high-fidelity text-to-speech with synthetic annotations](https://www.text-description-to-speech.com) by Dan Lyth and Simon King from Stability AI and the University of Edinburgh.

## Installation

1.  Navigate to the `sobits_tts` install directory.

    ```sh
    cd ~/colcon_ws/src/sobits_tts/install/
    ```

2.  Install the model.

    ```bash
    bash parler.sh
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Launch and Usage

1.  Launch `parler.launch.py` (Note: This may take some time).

    ```bash
    ros2 launch sobits_tts parler.launch.py
    ```

2.  Start the Action Client.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Parameters

### Supported Languages

Change **parler_tts_model_name** in [parler.launch.py](launch/parler.launch.py) to your desired language model.

| Language | Description | Model Name | Available Speakers |
| --- | --- | --- | --- |
| English | Mini (default) | `parler-tts/parler-tts-mini-v1` | \*34 selectable speakers |
| English | Mini Jenny | `parler-tts/parler-mini-v1-jenny` | Jenny only |
| English | Emotion-specifiable | `parler-tts/parler-tts-mini-expresso` | Jerry, Thomas, Talia, Elisabeth |
| English | CPU-optimized Jenny | `parler-tts/parler-tiny-v1-jenny` | Jenny only |
| Japanese | Mini | `2121-8/japanese-parler-tts-mini` | JSUT only |

<details>
<summary>* Full list of 34 available speakers for the English Mini model</summary>

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| Laura | Gary | Jon | Lea | Karen | Rick | Brenda |
| David | Eileen | Jordan | Mike | Yann | Joy | James |
| Eric | Lauren | Rose | Will | Jason | Aaron | Naomie |
| Alisa | Patrick | Jerry | Tina | Jenna | Bill | Tom |
| Carol | Barbara | Rebecca | Anna | Bruce | Emily |  |

</details>

> [!WARNING]
> If you are using a CPU-only PC, it will take time for speech to be generated, so it's recommended to use **CPU-optimized Jenny**.

If you want to use a different model, select one from [here](https://huggingface.co/models?other=parler_tts&sort=likes).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Speaker

In the **description** field of [parler.launch.py](launch/parler.launch.py), you can specify a particular speaker (recommended) or choose to have a random speaker each time.

  - Random Speaker: In the **description** field, specify the speaker as **male** or **female**.
      - Example:
        ```bash
        default_value="A female speaker delivers a slightly expressive and animated speech with a moderate speed and pitch. The recording is of very high quality, with the speaker's voice sounding clear and very close up."
        ```
  - Specific Speaker: In the **description** field, replace it with an "available speaker."
      - Example:
        ```bash
        default_value='Alisa.fast speed. Expression is rich. The speaking voice is noisy.',
        ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Speaking Style

You can modify the speaking style with simple text prompts like the following:

  - Example 1

    ```bash
    default_value='Will delivers a slightly expressive and animated speech with a moderate speed and pitch. The recording is of high quality, with the speaker voice sounding clear.',
    ```

  - Example 2

    ```bash
    default_value='Alisa.fast speed. Expression is rich. The speaking voice is noisy.',
    ```

  - To generate the highest quality audio, include the term "very clear audio"; for high levels of background noise, include "very noisy audio."

  - The remaining voice features (gender, speech rate, pitch, reverberation) can be directly controlled from the prompt.

  - The distance of the voice does not need to be specified as the volume does not change.

  - The output time does not change even if a random speaker is chosen.

  - About Emotion-Specifiable Models:

      - You can specify emotions such as "happy", "confused", "laughing", "sad", "whisper", "emphasis."

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Text to Speak

  - **End sentences with a period (.) or full stop (。).**
  - **For numbers, using words (e.g., "one", "two") is recommended over digits (e.g., "1", "2").**
  - Punctuation can be used to control the prosody of the generation (for example, commas can be used to add small breaks in the speech).
  - Generating a single word takes more time.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

# Open Audio TTS

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<a name="voicevox-top"></a>

# Voicevox TTS

[Voicevox](https://github.com/VOICEVOX/voicevox_core?tab=readme-ov-file) is a free, mid-quality text-to-speech and singing voice synthesis software.  
It only supports Japanese. If you want it to speak English, you can achieve this by writing the text in katakana.

## Installation
1. Move to the `install` directory of `sobits_tts`
    ```sh
    cd ~/colcon_ws/src/sobits_tts/install/
    ```

2. Install the model. Add `-g` at the end if you want to enable GPU.
    ```bash
    bash voicevox.sh
    ```

<p align="right">(<a href="#voicevox-top">Back to Voicevox TTS Top</a>)</p>

## Launch and Usage
1. Launch [voicevox.launch.py](launch/voicevox.launch.py)
    ```bash
    ros2 launch sobits_tts voicevox.launch.py
    ```

2. Start the Action Client

<p align="right">(<a href="#voicevox-top">Back to Voicevox TTS Top</a>)</p>

## Parameters
You can set the following parameters in [voicevox.launch.py](launch/voicevox.launch.py).

| Parameter | Name | Description | Default |
| --- | --- | --- | --- |
| Style ID | voicevox_style_id | Specifies the speaking style. Refer to the [VVM file and style ID mapping](https://github.com/VOICEVOX/voicevox_vvm/blob/main/README.md#%E9%9F%B3%E5%A3%B0%E3%83%A2%E3%83%87%E3%83%ABvvm%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%A8%E5%A3%B0%E3%82%AD%E3%83%A3%E3%83%A9%E3%82%AF%E3%82%BF%E3%83%BC%E3%82%B9%E3%82%BF%E3%82%A4%E3%83%AB%E5%90%8D%E3%81%A8%E3%82%B9%E3%82%BF%E3%82%A4%E3%83%AB-id-%E3%81%AE%E5%AF%BE%E5%BF%9C%E8%A1%A8). | 14 |
| VVM file name | voicevox_model_file_num | Specifies the speaker. Refer to the table above. | 1.vvm |
| Speech speed | voicevox_speed_scale | For example, 1.0 → 1.5 increases speed by 50%, 1.0 → 0.5 reduces speed by 50%. | 1.0 |
| Pitch scale | voicevox_pitch_scale | Higher values (e.g., +1.0) make the voice higher and cuter; negative values (e.g., -1.0) make the voice lower and calmer. | 0.0 |
| Intonation | voicevox_intonation_scale | Values closer to 0 produce flatter, more monotone speech. | 1.0 |
| Volume | voicevox_volume_scale | For example, 1.0 → 2.0 doubles the volume, 1.0 → 0.5 halves the volume. | 1.0 |
| Pre-speech silence | voicevox_pre_phoneme_length | For example, 0.3 adds 0.3 seconds of silence before speech starts. | 0.1 |
| Post-speech silence | voicevox_post_phoneme_length | For example, 0.3 adds 0.3 seconds of silence after speech ends. | 0.1 |
| Sampling rate | voicevox_output_sampling_rate | Higher values improve sound quality. | 48000 |
| Stereo output | voicevox_output_stereo | Whether to output stereo sound (split between left and right speakers for a spatial effect). | false |

<p align="right">(<a href="#voicevox-top">Back to Voicevox TTS Top</a>)</p>

<p align="right">(<a href="#readme-top">Back to Page Top</a>)</p>



