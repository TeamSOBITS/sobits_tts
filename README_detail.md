<a name="readme-top"></a>

[JP](README_detail.md) | [EN](README_detail.en.md)

[戻る](README.md)

<!-- 目次 -->
<details>
  <summary>目次</summary>
  <ol>
    <li><a href="#kokoro-tts">Kokoro TTS</a></li>
    <li><a href="#openpico">OpenPico (旧Text_to_Speech)</a></li>
    <li><a href="#coqui-tts">Coqui TTS</a></li>
    <li><a href="#parler-tts">Parler TTS</a></li>
  </ol>
</details>

# Kokoro TTS
Kokoroは，8,200万のパラメータを持つオープンウェイトのTTS（Text-to-Speech：音声合成）モデルです．
軽量なアーキテクチャにもかかわらず，大規模モデルに匹敵する品質を実現し，同時に処理速度とコスト効率を大幅に向上させています．

## インストール方法
1. sobits_ttsのinstallディレクトリに移動
    ```sh
    cd ~/colcon_ws/src/sobits_tts/install/
    ```

2. モデルをインストール
    ```bash
    bash kokoro.sh
    ```

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

## 実行・操作方法
1. [kokoro.launch.py](launch/kokoro.launch.py)を起動
    ```bash
    ros2 launch sobits_tts kokoro.launch.py
    ```

2. Action Clientを起動

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

## パラメータ

### 対応言語
kokoro_ttsは以下の言語に対応しています．\
[kokoro.launch.py](launch/kokoro.launch.py)の**kokoro_lang_code**を使用する言語に書き換えてください．

| 対応言語  | lang_code |
| ----- | ----- |
| アメリカ英語 | a |
| イギリス英語 | b |
| 日本語 | j |
| スペイン語 | e |
| フランス語 |f  |
| ヒンディー語 | h |
| イタリア語 | i |
| ブラジルのポルトガル語 | p |
| 中国語(普通話) | z |

* 中国語を使用する際は以下のコードを実行してください．
    ```sh
    pip3 install misaki[zh]==0.9.4
    ```
<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

### 話者
kokoro_ttsは言語別で様々な話者に対応しています．\
[kokoro.launch.py](launch/kokoro.launch.py)の**kokoro_voice**を使用する言語に書き換えてください．\
以下はその一例です．


- アメリカ英語
    - 女性
        - af_heart
        - af_bella
    - 男性
        - am_fenrir
        - am_puck
- 日本語
    - 女性
        - jf_alpha
    - 男性
        - jm_kumo

アメリカ英語や日本語，他の言語では，より多くの話者を指定できます．\
使用したい場合は[こちら](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md)を参考にしてください．

> 日本語を外国人が話しているように発話させることもできます．その場合は以下のように設定してください．
> - 言語(lang_code)：日本語
> - 話者(voice)：英語の話者
> - 発話するテキスト：日本語

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

### 発話速度
発話する速度を変更する場合は，[kokoro.launch.py](launch/kokoro.launch.py)の**kokoro_speech_speed**を書き換えてください．(デフォルト値：1.0)

例：1.2倍にしたい場合
```sh
kokoro_speech_speed_arg = DeclareLaunchArgument(
    'kokoro_speech_speed',
    default_value='1.2',
    description='Speech speed for Kokoro TTS. 0.5 for half speed, 2.0 for double speed.'
)
```
<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

### 区切る文字
特定の文字で区切らせて発話させる場合は，[kokoro.launch.py](launch/kokoro.launch.py)の**kokoro_split_regex**を書き換えてください．(デフォルト値：**r'[\n,.!?、。！？]+'**)

例：*で区切らせたい場合
```sh
kokoro_split_regex_arg = DeclareLaunchArgument(
    'kokoro_split_regex',
    default_value= r'[\n,.!?、。！？]+',
    description='Regular expression to split text'
)
```
<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

# OpenPico
OpenPicoはOpenJTalkとpico2waveを組み合わせたものです．
OpenJTalkは日本語のテキストを音声に変換するためのオープンソースの音声合成ソフトウェアです．
pico2waveは様々な言語に対応した軽量なテキスト音声変換（TTS）エンジンです．


## インストール方法
1. sobits_ttsのinstallディレクトリに移動
    ```sh
    cd ~/colcon_ws/src/sobits_tts/install/
    ```

2. モデルをインストール
    ```bash
    bash openpico.sh
    ```

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

## 実行・操作方法
1. [openpico.launch.py](launch/openpico.launch.py)を起動
    ```bash
    ros2 launch sobits_tts openpico.launch.py
    ```

2. Action Clientを起動

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

## パラメータ
### 対応言語
OpenPicoは以下の言語に対応しています．\
[openpico.launch.py](launch/openpico.launch.py)の**openpico_language**を使用する言語に書き換えてください．

| 対応言語  | openpico_language |
| ----- | ----- |
| 英語 | en |
| 日本語 | ja |

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

### 話者
OpenPicoは日本語のみ様々な話者に対応しています．\
[openpico.launch.py](launch/openpico.launch.py)の**openpico_voice_data_ja**を使用する話者のファイルパスに書き換えてください．\

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

# Coqui TTS
Coqui TTSは，テキストから音声を生成するためのオープンソースの音声合成ツールキットです．

## インストール方法
1.  sobits_ttsのinstallディレクトリに移動
    ```sh
    cd ~/colcon_ws/src/sobits_tts/install/
    ```
2.  モデルをインストール
    ```bash
    bash coqui.sh
    ```
3. TTSサーバーを簡単に実行するために， `alias` を作成する.
    - **CPUのみ**の場合:
    ```sh
    $ echo "alias tts_launch='docker run --rm -it -p 5002:5002 -v ~/{PATH_ROS_WS_LOCAL}/src/coqui_tts_ros/models/:/root/.local/share/tts/ --entrypoint \"tts-server\" ghcr.io/coqui-ai/tts-cpu'" >> ~/.bash_alias
    ```
    - **GPU**の場合:
    ```sh
    $ echo "alias tts_launch='docker run --rm -it -p 5002:5002 --gpus all -v ~/{PATH_ROS_WS_LOCAL}/src/coqui_tts_ros/models/:/root/.local/share/tts/ --entrypoint \"tts-server\" ghcr.io/coqui-ai/tts'" >> ~/.bash_alias
    ```
> [!IMPORTANT]
> `{PATH_ROS_WS_LOCAL}` は**ローカル環境**に存在するROSのワークスペースのPATHである．

> [!IMPORTANT]
> すでに，Dockerのコンテナーの中にいる場合，ローカル環境上でコマンド6を実行する必要がある．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

## 実行・操作方法
1. **ローカル環境**上でTTSサーバーを立ち上げる．
    - **CPUのみ**の場合:
    ```sh
    $ tts_launch --model_name tts_models/en/vctk/vits
    ```
    - **GPU**の場合:
    ```sh
    $ tts_launch --model_name tts_models/en/vctk/vits --use_cuda true
    ```

2.  [coqui.launch.py](launch/coqui.launch.py)を起動
    ```bash
    ros2 launch sobits_tts coqui.launch.py
    ```
3.  Action Clientを起動

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

## パラメータ
[coqui.launch.py](launch/coqui.launch.py)で以下のパラメータを指定できます．

| パラメータ  | パラメータ名 | 説明 | デフォルト値 |
| ----- | ----- | ----- | ----- |
| 対応言語 | coqui_language_id | 使用する言語のID (英語のみ) | |
| 話者 | coqui_speaker_id | 使用する話者のID (p225 ~ p376) | p225 |
| 句読点の自動追加 | coqui_add_stop_char | テキストの最後に句読点を自動追加するかどうか | True |

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

# Parler TTS
Parler_TTSは，特定のスピーカーのスタイル(性別，ピッチ，話し方など)で高品質で自然な音声を生成できる軽量のテキスト読み上げ(TTS)モデルです．

Stability AIとエジンバラ大学のDan LythとSimon Kingによる論文[Natural language guidance of high-fidelity text-to-speech with synthetic annotations](https://www.text-description-to-speech.com) からの複製されました．

## インストール方法
1. sobits_ttsのinstallディレクトリに移動
    ```sh
    cd ~/colcon_ws/src/sobits_tts/install/
    ```

2. モデルをインストール
    ```bash
    bash parler.sh
    ```

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

## 実行・操作方法
1. [parler.launch.py](launch/parler.launch.py)を起動 (時間がかかるので注意)
    ```bash
    ros2 launch sobits_tts parler.launch.py
    ```

2. Action Clientを起動

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

## パラメータ
### 対応言語
[parler.launch.py](launch/parler.launch.py)の**parler_tts_model_name**を使用する言語モデルに書き換えてください．

| 言語 | 説明 | モデル名 | 利用可能な話者 |
| --- | --- | --- | --- |
| 英語 | ミニ(デフォルト) | parler-tts/parler-tts-mini-v1 | *34人から指定可能|
| 英語 | ミニジェニー | parler-tts/parler-mini-v1-jenny | Jennyのみ |
| 英語 | 感情指定可能 | parler-tts/parler-tts-mini-expresso | Jerry, Thomas, Talia, | 英語 Elisabeth |
| 英語 | CPU向けジェニー | parler-tts/parler-tiny-v1-jenny | Jennyのみ |
| 日本語 | ミニ |2121-8/japanese-parler-tts-mini | JSUTのみ |

<details>
 <summary>* 英語のミニモデルで利用可能な34人の話者の全リスト(英語)</summary>

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| Laura | Gary | Jon | Lea | Karen | Rick | Brenda |
| David | Eileen | Jordan | Mike | Yann | Joy | James |
| Eric | Lauren | Rose | Will | Jason | Aaron | Naomie |
| Alisa | Patrick | Jerry | Tina | Jenna | Bill | Tom |
| Carol | Barbara | Rebecca | Anna | Bruce | Emily |  |
</details>

> [!WARNING]
> CPUのみのPCを使用している場合，発話までに時間がかかるため，**CPU向けジェニー**の使用を推奨します．

別のモデルを使用したい場合は[こちら](https://huggingface.co/models?other=parler_tts&sort=likes)から選択してください．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

### 話者
[parler.launch.py](launch/parler.launch.py)の**description**の項目で，特定の話者(推奨)か，毎回ランダムな話者にするかを指定できます．

- ランダムな話者：**description**の項目で，話者を**male**か**female**と指定してください．
  - 例
      ``` bash
      default_value="A female speaker delivers a slightly expressive and animated speech with a moderate speed and pitch. The recording is of very high quality, with the speaker's voice sounding clear and very close up."
      ```
- 特定の話者：**description**の項目で，「利用可能な話者」に置き換えてください．
  - 例
      ``` bash
      default_value='Alisa.fast speed. Expression is rich. The speaking voice is noisy.',
      ```

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

### 話し方
次のような単純なテキストプロンプトで話し方を変更することができます．
- 例1

    ``` bash
    default_value='Will delivers a slightly expressive and animated speech with a moderate speed and pitch. The recording is of  high quality, with the speaker voice sounding clear.',
    ```
- 例2
    ``` bash
    default_value='Alisa.fast speed. Expression is rich. The speaking voice is noisy.',
    ```

- 最高品質のオーディオを生成するには「very clear audio」という用語を含め，高レベルのバックグラウンドノイズには「very noisy audio」という用語を含めます
- 残りの音声機能(性別，発話速度，ピッチ，残響)は，プロンプトから直接制御できます
- 声の大きさが変わらないため声の距離の指定は必要ない
- 話者をランダムにしても出力時間は変化なし

- 感情指定可能モデルについて
    - "happy", "confused", "laughing", "sad", "whisper", "emphasis"などの感情を指定できます.

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

## 発話させる文章について

- **文末にピリオド(.)あるいは句点(。)をつけてください．**
- **数字について，半角(1, 2など)より，one, 二などを推奨**
- 句読点は，世代の韻律を制御するために使用できます(たとえば，カンマを使用して音声に小さな区切りを追加します)
- 1単語のみ発話させる場合は生成に時間がかかります

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>