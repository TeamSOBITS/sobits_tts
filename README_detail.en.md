<a name="readme-top"></a>

[JP](README.md) | [EN](README.en.md)

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

# SOBITS TTS

# 作成中
<!-- 目次 -->
<details>
  <summary>目次</summary>
  <ol>
    <li>
      <a href="#概要">概要</a>
    </li>
    <li>
      <a href="#セットアップ">セットアップ</a>
      <ul>
        <li><a href="#環境条件">環境条件</a></li>
        <li><a href="#インストール方法">インストール方法</a></li>
      </ul>
    </li>
    <li><a href="#実行操作方法">実行・操作方法</a></li>
    <li><a href="#マイルストーン">マイルストーン</a></li>
  </ol>
</details>

<!-- レポジトリの概要 -->
## 概要
SOBITS TTSは様々なText to Speech (TTS)をROS2のAction通信に対応させ，まとめたものです．

現在以下のTTSに対応しています．
- Kokoro TTS
- Open JTalk (旧Text to Speech)
- SVOX Pico TTS (旧Text to Speech)
- Parler TTS
- Coqui TTS

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

<!-- セットアップ -->
## セットアップ
ここで，本レポジトリのセットアップ方法について説明します．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

### 環境条件
まず，以下の環境を整えてから，次のインストール方法に進んでください．
| System  | Version |
| --- | --- |
| Ubuntu | 22.04 (Jammy Jellyfish) |
| ROS    | Humble Hawksbill |
| Python | 3.10 |

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

### インストール方法
1. ROS2の`src`フォルダに移動します．
    ```sh
    cd ~/colcon_ws/src/
    ```

2. 本レポジトリをcloneします．
    ```sh
    git clone -b humble-devel https://github.com/TeamSOBITS/sobits_tts.git
    ```
3. レポジトリの中へ移動します．
    ```sh
    cd sobits_tts/
    ```
4. 依存パッケージをインストールします．
    ```sh
    bash install.sh
    ```
5. パッケージをコンパイルします．
    ```sh
    cd ~/colcon_ws/
    ```
    ```sh
    colcon build --symlink-install
    ```
    ```sh
    source ~/colcon_ws/install/setup.sh
    ```

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

<!-- 実行・操作方法 -->
## 実行・操作方法

実行する前に，使用するTTSのモデルをダウンロードする必要があります．

各TTS名をクリックするとダウンロードと実行方法を閲覧できます．

| TTS名                       | 精度 | 生成速度 | 特徴 | 
| ---                         | -- |--- |--- |
| [Kokoro]()                      | ○ | ○ |--- |
| [OpenPico (旧Text to Speech)]() | △ | ◎ |--- |
| [Parler]()                     | ◎ | △ | 感情指定が可能なモデルあり |
| [Coqui]()                       | --- |--- |--- |


<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

## マイルストーン
- [ ] 以下のTTSに対応
  - [ ] Fish Speech
  - [ ] VOICEVOX

現時点のバグや新規機能の依頼を確認するためにIssueページ をご覧ください．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

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