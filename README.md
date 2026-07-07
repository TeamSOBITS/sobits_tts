<a name="readme-top"></a>

[JA](README.ja.md) | [EN](README.md)

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

# SOBITS TTS

<details>
<summary>Table of Contents</summary>
<ol>
<li><a href="#introduction">Introduction</a></li>
<li><a href="#getting-started">Getting Started</a>
<ul>
<li><a href="#prerequisites">Prerequisites</a></li>
<li><a href="#installation">Installation</a></li>
</ul>
</li>
<li><a href="#launch-and-usage">Launch and Usage</a></li>
<li><a href="#milestones">Milestones</a></li>
</ol>
</details>

## Introduction

SOBITS TTS integrates various Text-to-Speech (TTS) engines with ROS2 Action communication.

Currently, it supports the following TTS engines:
- Kokoro TTS
- Coqui TTS
- Piper TTS
- Supertonic TTS
- Voicevox TTS
- Open JTalk, SVOX Pico TTS
- Parler TTS
- Open Audio TTS

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

This section explains how to set up this repository.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Prerequisites

First, ensure you have the following environment set up before proceeding with the installation method.
| System  | Version |
| --- | --- |
| Ubuntu | 24.04 (Noble Numbat) |
| ROS    | Jazzy Jalisco |
| Python | 3.12 |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Installation

1.  Navigate to your ROS2 `src` folder.

    ```sh
    cd ~/colcon_ws/src/
    ```

2.  Clone this repository.

    ```sh
    git clone -b jazzy-devel https://github.com/TeamSOBITS/sobits_tts.git
    ```

3.  Move into the repository directory.

    ```sh
    cd sobits_tts/
    ```

4.  Install the dependent packages.

    ```sh
    bash install.sh
    ```

5.  Compile the package.

    ```sh
    cd ~/colcon_ws/
    ```

    ```sh
    colcon build --symlink-install
    ```

    ```sh
    source ~/colcon_ws/install/setup.sh
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Launch and Usage

Before running, you need to download the models for the TTS engine you intend to use.

Click on each TTS name to view download and execution instructions.

| TTS Name                       | Accuracy | Generation Speed | Features | 
| ---                         | -- |--- |--- |
| [Kokoro](https://github.com/TeamSOBITS/sobits_tts/blob/jazzy-devel/README_detail.md#kokoro-tts)                      | ☆☆☆☆  | ☆☆☆☆ | Supports English, Japanese, etc. |
| [Coqui](https://github.com/TeamSOBITS/sobits_tts/blob/jazzy-devel/README_detail.md#coqui-tts)                       | ☆☆☆☆   | ☆☆☆☆ | Supports only English. |
| [Piper](https://github.com/TeamSOBITS/sobits_tts/blob/jazzy-devel/README_detail.md#piper-tts)                     | ☆☆☆     | ☆☆☆☆☆ | Supports multiple languages beyond Japanese. Ultra-lightweight and high-speed operation even on a CPU.　|
| [Supertonic](https://github.com/TeamSOBITS/sobits_tts/blob/jazzy-devel/README_detail.md#supertonic-tts)                  | ☆☆☆     | ☆☆☆☆☆ | Supports 31 languages including English and Japanese, extremely lightweight.　|
| [Voicevox](https://github.com/TeamSOBITS/sobits_tts/blob/jazzy-devel/README_detail.md#voicevox-tts)                    | ☆☆☆☆   | ☆☆☆☆| Supports only Japanese; speech is available with Zundamon voice　|
| [OpenPico](https://github.com/TeamSOBITS/sobits_tts/blob/jazzy-devel/README_detail.md#openpico)                        | ☆        | ☆☆☆☆☆ | Supports English and Japanese. |
| [Parler](https://github.com/TeamSOBITS/sobits_tts/blob/jazzy-devel/README_detail.md#parler-tts)                      | ☆☆☆☆   | ☆ | Supports English, Japanese, etc. Includes models with emotion specification | 
| [OpenAudio](https://github.com/TeamSOBITS/sobits_tts/blob/jazzy-devel/README_detail.md#open-audio-tts)                  | ☆☆☆☆☆ | ☆ | Supports English, Japanese, etc., voice cloning, and emotion specification. |

### Common Parameters

| Parameter | Description | Default |
| --- | --- | --- |
| speaker_volume | Sets the speaker output volume as a percentage. Returns to the original volume after shutdown. (e.g., `"150%"`) | `""` |

> [!NOTE]
> `speaker_volume` is now implemented by changing the default output sink volume with `pactl set-sink-volume`,
> not by applying software gain to the generated WAV data.
> If you change the output device in the GUI after the server starts, the node will manage and restore the sink volume captured at startup.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Milestones
Please refer to the [Issue page](https://github.com/TeamSOBITS/sobits_tts/issues) for current bugs and feature requests.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/TeamSOBITS/sobits_tts.svg?style=for-the-badge
[contributors-url]: https://github.com/TeamSOBITS/sobits_tts/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/TeamSOBITS/sobits_tts.svg?style=for-the-badge
[forks-url]: https://github.com/TeamSOBITS/sobits_tts/network/members
[stars-shield]: https://img.shields.io/github/stars/TeamSOBITS/sobits_tts.svg?style=for-the-badge
[stars-url]: https://github.com/TeamSOBITS/sobits_tts/stargazers
[issues-shield]: https://img.shields.io/github/issues/TeamSOBITS/sobits_tts.svg?style=for-the-badge
[issues-url]: https://github.com/TeamSOBITS/sobits_tts/issues
[license-shield]: https://img.shields.io/github/license/TeamSOBITS/sobits_tts.svg?style=for-the-badge
[license-url]: LICENSE
