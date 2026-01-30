<a name="readme-top"></a>

[JA](README_detail.md) | [EN](README_detail.en.md)

[Back](README.en.md)



<details>
<summary>Table of Contents</summary>
<ol>
<li><a href="#kokoro-tts">Kokoro TTS</a></li>
<li><a href="#openpico">OpenPico (formerly Text_to_Speech)</a></li>
<li><a href="#coqui-tts">Coqui TTS</a></li>
<li><a href="#parler-tts">Parler TTS</a></li>
<li><a href="#open-audio-tts">Open Audio TTS</a></li>
<li><a href="#voicevox-tts">Voicevox TTS</a></li>
<li><a href="#supertonic-tts">Supertonic TTS</a></li>
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


## Other Parameters

The following parameters can be configured in [kokoro.launch.py](launch/kokoro.launch.py).

| Parameter | Description | Default |
| --- | --- | --- |
| `kokoro_speech_speed` | Speaking speed. For example, set to `1.2` for 1.2x speed. | 1.0 |
| `kokoro_split_regex` | Regex pattern for splitting text. The model processes and speaks text segmented by these characters. | `r'[\n,.!?、。！？]+'` |
| `kokoro_device` | Computing device to use (`cpu` or `cuda:0`). If left empty, it automatically selects GPU if available, otherwise falls back to CPU. | `''` |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

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
    $ echo "alias tts_launch='docker run --rm -it -p 5002:5002 -v ~/{PATH_ROS_WS_LOCAL}/src/sobits_tts/install/coqui/models/:/root/.local/share/tts/ --entrypoint \"tts-server\" ghcr.io/coqui-ai/tts-cpu'" >> ~/.bash_alias
    ```
      - For **GPU**:
    <!-- end list -->
    ```sh
    $ echo "alias tts_launch='docker run --rm -it -p 5002:5002 --gpus all -v ~/{PATH_ROS_WS_LOCAL}/src/sobits_tts/install/coqui/models/:/root/.local/share/tts/ --entrypoint \"tts-server\" ghcr.io/coqui-ai/tts'" >> ~/.bash_alias
    ```

> [!IMPORTANT]
> `{PATH_ROS_WS_LOCAL}` is the **local path** to your ROS workspace.

> [!IMPORTANT]
> If you are already inside a Docker container, you need to run command 3 on your local machine.

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

Open Audio TTS supports zero-shot and few-shot voice cloning, as well as various emotions, tones, and special markers. **You can reproduce a recorded voice and make it speak any text you want in that voice.**

Using a GPU with 8GB or more of VRAM is recommended.

Open Audio TTS supports the following languages. Language is automatically detected, so no configuration is needed.

| | | | |
| --- | --- | --- | --- |
| English | Chinese | Japanese | German |
| French | Spanish | Korean | Arabic |
| Russian | Dutch | Italian | Polish |
| Portuguese | | | |

<p align="right">(<a href="#openaudio-top">Return to Open Audio TTS Top</a>)</p>

## Installation Guide

1.  **Create a [Hugging Face](https://huggingface.co/) Account**

    Access the link above and create an account via "Sign Up". If you already have an account, proceed to step 2.

2.  **Access the Model Page and Agree to the Terms**

    Go to the [model page](https://huggingface.co/fishaudio/openaudio-s1-mini) and agree to the terms. Look for a section that says something like:

    `You need to agree to share your contact information to access this model.`

3.  **Create a Hugging Face Access Token**

    Go to the [Hugging Face settings page](https://huggingface.co/settings/tokens).
    Click "New token" and set the following options:

      - **Token type**: `fine-grained`
      - **Token name**: `Any name you like`
      - **User Permissions**:
          - `Repositories`: `Read access to contents of all public gated repos you can access`
          - `Inference`: `Make calls to Inference Providers`

    After setting, click "Create token" to generate your token.

4.  **Open a terminal and navigate to the `sobits_tts` install directory.**

    ```sh
    cd ~/colcon_ws/src/sobits_tts/install/
    ```

5.  **Install dependencies**

    ```bash
    bash openaudio.sh
    ```

<p align="right">(<a href="#openaudio-top">Return to Open Audio TTS Top</a>)</p>

## Execution and Usage

There are three main ways to use the service.

  - Using it as a standard TTS
  - Cloning and speaking with a voice recorded via a microphone
  - Cloning and speaking with a pre-existing WAV file

### Using It as a Standard TTS

1.  Launch `openaudio.launch.py`.
    ```sh
    ros2 launch sobits_tts openaudio.launch.py
    ```
2.  Launch the Action Client.

<p align="right">(<a href="#openaudio-top">Return to Open Audio TTS Top</a>)</p>

### Cloning a Microphone-Recorded Voice

1.  In Ubuntu settings, set your microphone as the sound input device.
2.  Open a terminal, navigate to the `test` directory, and run `recorder.py` to record.
    ```sh
    cd ~/colcon_ws/src/sobits_tts/test/
    python3 recorder.py
    ```
3.  In `openaudio.launch.py`, change the `reference_audio_path` to the **absolute path of the `record.wav` file** created in the `soundfile` directory.
4.  Launch `openaudio.launch.py`.
    ```sh
    ros2 launch sobits_tts openaudio.launch.py
    ```
5.  Launch the Action Client.

<p align="right">(<a href="#openaudio-top">Return to Open Audio TTS Top</a>)</p>

### Cloning a Pre-existing WAV File

1.  In `openaudio.launch.py`, change the `reference_audio_path` to the **absolute path of your WAV file**.
2.  Launch `openaudio.launch.py`.
3.  Launch the Action Client.

## Parameters

### Controlling Emotion, Tone, and Speed

You can control emotion, speaking speed, and tone by adding tags to the text you want to speak. For more details, refer to the [official documentation](https://docs.fish.audio/emotion-control/tts-emotion-and-control-tags-user-guide).

Emotion tags are placed at the beginning of a sentence, while tone and special markers can be placed anywhere.

Examples:

  - **Emotion Tag Usage**: `(Happy)How are you today?`
  - **Tone Marker**: `Help! (shouting) Hey!`
  - **Special Marker**: `What! (laughing) Ha,ha,ha!`

<details>
<summary>All Configurable Tags</summary>

1.  **Emotion Markers (only at the beginning of a sentence)**

    `  (angry) (sad) (disdainful) (excited) (surprised) (satisfied) (unhappy) (anxious) (hysterical) (delighted) (scared) (worried) (indifferent) (upset) (impatient) (nervous) (guilty) (scornful) (frustrated) (depressed) (panicked) (furious) (empathetic) (embarrassed) (reluctant) (disgusted) (keen) (moved) (proud) (relaxed) (grateful) (confident) (interested) (curious) (confused) (joyful) (disapproving) (negative) (denying) (astonished) (serious) (sarcastic) (conciliative) (comforting) (sincere) (sneering) (hesitating) (yielding) (painful) (awkward) (amused) `

2.  **Tone Markers (can be placed anywhere)**

    `(in a hurry tone) (shouting) (screaming) (whispering) (soft tone)`

3.  **Special Markers (can be placed anywhere)**

    `(laughing) (chuckling) (sobbing) (crying loudly) (sighing) (panting) (groaning) (crowd laughing) (background laughter) (audience laughing)`

</details>

<p align="right">(<a href="#openaudio-top">Return to Open Audio TTS Top</a>)</p>

### About Voice Cloning

You can change the reference audio even after launching the service with the following command. **Be sure to replace it with the absolute path of your reference audio file.**

```sh
ros2 param set /tts_action_server openaudio_tts.reference_audio_path ${absolute_path_to_reference_audio}
```

Similarly, you can change the text corresponding to the reference audio after launch:

```sh
ros2 param set /tts_action_server openaudio_tts.reference_text ${text_corresponding_to_reference_audio}
```

Here are the recommended conditions for reference audio. For more details, refer to the [official documentation](https://docs.fish.audio/text-to-speech/voice-clone-best-practices).

  - A single speaker only
  - Stable volume, tone, and emotion
  - Short pauses (0.5 seconds recommended)
  - **For Simple Voice Cloning**
      - 30-45 seconds of high-quality audio
      - **Best**: 2-3 audio clips of 15-20 seconds each that form a complete paragraph
  - **For High-Quality Voice Cloning**
      - 30-180 minutes of high-quality audio
      - Multiple languages and emotions
      - No background noise
      - High recording quality
      - No echo

<p align="right">(<a href="#openaudio-top">Return to Open Audio TTS Top</a>)</p>

## Configurable Parameters in the Launch File

The following parameters can be set in `openaudio.launch.py`.
You can also dynamically change parameters after launching the file with commands like the one below.

Example: To change the absolute path of the reference audio file for voice cloning:

```sh
ros2 param set /tts_action_server openaudio_tts.reference_audio_path
```

| Parameter Name                 | Description                                                                       | Impact of Change                                                                                                                                                                     | Default Value      |
| ------------------------------ | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------ |
| `reference_audio_path`         | The absolute path to the reference audio file for voice cloning.                  | When specified, the model learns the tone and voice quality of that audio and applies it to the output.                                                                                | `""`                 |
| `reference_text`               | The text spoken in the reference audio.                                           | Setting this improves accuracy but slows down generation speed.                                                                                                                      | `""`                 |
| `reference_id`                 | An identifier for the reference data.                                             | Allows for distinguishing and managing multiple references by ID. An empty value means no identifier.                                                                                | `None`             |
| `seed`                         | A random seed to ensure speaker reproducibility.                                  | When specified, it always speaks with the same speaker. A value of 0 or `None` will result in a completely random speaker.                                                            | `None`             |
| `use_memory_cache`             | Whether to cache intermediate results in memory.                                  | Enabling the cache speeds up processing but increases memory usage.                                                                                                                  | `False`            |
| `chunk_length`                 | The number of characters per chunk when splitting text for inference.             | A smaller value starts the response sooner but can result in more fragmented splits, potentially losing context. A larger value increases memory consumption.                          | `200`              |
| `normalize`                    | Whether to perform normalization to ensure consistent volume of the output waveform. | If `False`, the output audio volume may vary, depending on the volume of the original recording.                                                                                     | `True`             |
| `max_new_tokens`               | The upper limit on the number of new tokens to generate.                          | A smaller limit may result in shorter outputs or premature termination. A larger limit increases processing time and memory usage.                                                       | `512`              |
| `top_p`                        | The kernel sampling probability controlling the diversity and certainty of the generated text. | A smaller value (e.g., 0.3) reduces output diversity and increases stability. A larger value increases diversity.                                                                   | `0.65`             |
| `repetition_penalty`           | A value to suppress the repetition of the same phrases.                           | A larger value reduces the repetition of identical expressions, but it may also negatively affect the natural flow of sentences.                                                         | `1.1`              |
| `temperature`                  | The temperature coefficient to adjust the randomness of the generated text.         | A low value (e.g., 0.2) results in a stable output, like a news broadcast. A value of 0.9 or higher adopts rarer words, creating a more character-rich delivery. | `0.8`              |

The following parameters **cannot be changed dynamically** after launching the service.

| Parameter Name                 | Description                                                                                             | Impact of Change                                                                                                                                                                     | Default Value      |
| ------------------------------ | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------ |
| `use_half_precision`           | Whether to use half-precision (FP16) for inference.                                                     | Improves speed and reduces memory usage, but may slightly degrade sound quality or stability.                                                                                        | `True`             |
| `device`                       | The inference device to use (`cuda` or `cpu`).                                                          | `cpu` is slower than GPU but works universally. `cuda` enables faster processing and FP16 usage.                                                                                   | `cuda`             |
| `compile_model`                | Whether to apply `torch.compile()` to speed up the model.                                               | Enabling this speeds up inference but requires a compilation time during the initial load.                                                                                         | `False`            |
| `max_text_length`              | The maximum number of characters for input text.                                                        | Text exceeding this length is truncated and split into multiple chunks, requiring care for consistent long-text generation but reducing processing load.                          | `256`              |
| `listen_address`               | The IP address and port where the TTS server accepts requests.                                          | Changing the address alters the network interface and connection range where the server listens.                                                                                     | `0.0.0.0:8080`     |

<p align="right">(<a href="#openaudio-top">Return to Open Audio TTS Top</a>)</p>




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

After launching the launch file, you can still dynamically change parameters using the following command.

Example: To change the style ID to 2

```sh
ros2 param set /tts_action_server voicevox.style_id 1
```


| Parameter | Name | Description | Default |
| --- | --- | --- | --- |
| Style ID | voicevox_style_id | Specifies the speaking style. Refer to the [VVM file and style ID mapping](https://github.com/VOICEVOX/voicevox_vvm/blob/main/README.md#%E9%9F%B3%E5%A3%B0%E3%83%A2%E3%83%87%E3%83%ABvvm%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%A8%E5%A3%B0%E3%82%AD%E3%83%A3%E3%83%A9%E3%82%AF%E3%82%BF%E3%83%BC%E3%82%B9%E3%82%BF%E3%82%A4%E3%83%AB%E5%90%8D%E3%81%A8%E3%82%B9%E3%82%BF%E3%82%A4%E3%83%AB-id-%E3%81%AE%E5%AF%BE%E5%BF%9C%E8%A1%A8). | 3 |
| VVM file name | voicevox_model_file_num | Specifies the speaker. Refer to the table above. | 0.vvm |
| Speech speed | voicevox_speed_scale | For example, 1.0 → 1.5 increases speed by 50%, 1.0 → 0.5 reduces speed by 50%. | 1.0 |
| Pitch scale | voicevox_pitch_scale | Higher values (e.g., +1.0) make the voice higher and cuter; negative values (e.g., -1.0) make the voice lower and calmer. | 0.0 |
| Intonation | voicevox_intonation_scale | Values closer to 0 produce flatter, more monotone speech. | 1.0 |
| Volume | voicevox_volume_scale | For example, 1.0 → 2.0 doubles the volume, 1.0 → 0.5 halves the volume. | 1.0 |
| Pre-speech silence | voicevox_pre_phoneme_length | For example, 0.3 adds 0.3 seconds of silence before speech starts. | 0.1 |
| Post-speech silence | voicevox_post_phoneme_length | For example, 0.3 adds 0.3 seconds of silence after speech ends. | 0.1 |
| Sampling rate | voicevox_output_sampling_rate | Higher values improve sound quality. | 48000 |
| Stereo output | voicevox_output_stereo | Whether to output stereo sound (split between left and right speakers for a spatial effect). | false |

<p align="right">(<a href="#voicevox-top">Back to Voicevox TTS Top</a>)</p>

<a name="supertonic-top"></a>

# Supertonic TTS

[Supertonic TTS](https://github.com/supertone-inc/supertonic) is a lightning-fast, on-device text-to-speech system designed for extreme performance with minimal computational overhead. Powered by ONNX Runtime, it runs entirely on your device and is even compatible with Raspberry Pi.

## Installation
1. Move to the `install` directory of `sobits_tts`
    ```sh
    cd ~/colcon_ws/src/sobits_tts/install/
    ```

2. Install the model. 
    ```bash
    bash supertonic.sh
    ```

<p align="right">(<a href="#supertonic-top">Back to Supertonic TTS Top</a>)</p>

## Launch and Usage
1. Launch [supertonic.launch.py](launch/supertonic.launch.py)
    ```sh
    ros2 launch sobits_tts supertonic.launch.py
    ```

2. Start the Action Client

<p align="right">(<a href="#supertonic-top">Back to Supertonic TTS Top</a>)</p>

## Parameters
You can set the following parameters in [supertonic.launch.py](launch/supertonic.launch.py).

After launching the launch file, you can still dynamically change parameters using the following

Example: To change the supertonic.voice_name to M1

```sh
ros2 param set /tts_action_server supertonic.voice_name M1
```

| Parameter Name | Description | Default Value |
| --- | --- | --- |
| supertonic_device | The computing device to use (cpu or cuda). If left empty, it prioritized the GPU if available; otherwise, the CPU is automatically selected. | 'cpu' |
| supertonic_voice_name | Speaker selection. Available options: M1, M2, M3, M4, M5, F1, F2, F3, F4, F5. | 'F1' |
| supertonic_language | Language code. Choose from `en`, `ko`, `es`, `pt`, or `fr`. | 'en' |
| supertonic_total_steps | Number of denoising steps. Increasing this improves audio quality but slows down generation time. | 5 |
| supertonic_speed | Speech speed. For example, set to `1.2` for 1.2x speed. Higher values may lead to skipped words. | 1.05 |
| supertonic_max_chunk_length | The maximum number of characters to process in a single chunk. | 300 |
| supertonic_silence_duration | The duration of silence (in seconds) to insert between sentences. | 0.3 |

Supports 5 languages—English, Korean, Spanish, Portuguese, and French—while remaining extremely lightweight.

<p align="right">(<a href="#supertonic-top">Back to Supertonic TTS Top</a>)</p>

<p align="right">(<a href="#readme-top">Back to Page Top</a>)</p>