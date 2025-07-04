<a name="readme-top"></a>

[JP](README.md) | [EN](README.en.md)

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
  - Open JTalk, SVOX Pico TTS (formerly Text to Speech)
  - Parler TTS
  - Coqui TTS

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

This section explains how to set up this repository.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Prerequisites

First, ensure you have the following environment set up before proceeding with the installation method.
| System  | Version |
| --- | --- |
| Ubuntu | 22.04 (Jammy Jellyfish) |
| ROS    | Humble Hawksbill |
| Python | 3.10 |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Installation

1.  Navigate to your ROS2 `src` folder.

    ```sh
    cd ~/colcon_ws/src/
    ```

2.  Clone this repository.

    ```sh
    git clone -b humble-devel https://github.com/TeamSOBITS/sobits_tts.git
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

| TTS Name                    | Accuracy | Generation Speed | Features                               |
| ---                         | --       | ---              | ---                                    |
| [Kokoro](https://github.com/TeamSOBITS/sobits_tts/blob/humble-devel/README_detail.md#kokoro-tts)                      | ◯        | ◯                | ---                                    |
| [OpenPico (formerly Text to Speech)](https://github.com/TeamSOBITS/sobits_tts/blob/humble-devel/README_detail.md#openpico) | △        | ◎                | ---                                    |
| [Coqui](https://github.com/TeamSOBITS/sobits_tts/blob/humble-devel/README_detail.md#coqui-tts)                       | ◯        | ◯                | ---                                    |
| [Parler](https://github.com/TeamSOBITS/sobits_tts/blob/humble-devel/README_detail.md#parler-tts)                     | ◎        | △                | Includes models with emotion specification |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Milestones

  - [ ] Support for the following TTS engines:
      - [ ] Fish Speech
      - [ ] VOICEVOX

Please refer to the Issue page for current bugs and feature requests.

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