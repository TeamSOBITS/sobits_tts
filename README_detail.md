<a name="readme-top"></a>

[JA](README_detail.md) | [EN](README_detail.en.md)

[戻る](README.md)

<!-- 目次 -->
<details>
  <summary>目次</summary>
  <ol>
    <li><a href="#kokoro-tts">Kokoro TTS</a></li>
    <li><a href="#openpico">OpenPico (旧Text_to_Speech)</a></li>
    <li><a href="#coqui-tts">Coqui TTS</a></li>
    <li><a href="#parler-tts">Parler TTS</a></li>
    <li><a href="#open-audio-tts">Open Audio TTS</a></li>
    <li><a href="#voicevox-tts">Voicevox TTS</a></li>
    <li><a href="#supertonic-tts">Supertonic TTS</a></li>
    <li><a href="#piper-tts">Piper TTS</a></li>
  </ol>
</details>

<a name="kokoro-top"></a>

# Kokoro TTS
[Kokoro](https://huggingface.co/hexgrad/Kokoro-82M)は，8,200万のパラメータを持つオープンウェイトのTTS（Text-to-Speech：音声合成）モデルです．
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

<p align="right">(<a href="#kokoro-top">Kokoro TTSトップに戻る</a>)</p>

## 実行・操作方法
1. [kokoro.launch.py](launch/kokoro.launch.py)を起動
    ```bash
    ros2 launch sobits_tts kokoro.launch.py
    ```

2. Action Clientを起動

<p align="right">(<a href="#kokoro-top">Kokoro TTSトップに戻る</a>)</p>

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

* 中国語を使用する際は以下のコマンドを実行してください．
    ```sh
    pip3 install misaki[zh]==0.9.4
    ```
<p align="right">(<a href="#kokoro-top">Kokoro TTSトップに戻る</a>)</p>

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

<p align="right">(<a href="#kokoro-top">Kokoro TTSトップに戻る</a>)</p>

## その他のパラメータ

以下は[kokoro.launch.py](launch/kokoro.launch.py)で設定可能なその他のパラメータです．

| パラメータ名 | 説明 | デフォルト値 |
| --- | --- | --- |
| kokoro_speech_speed | 発話する速度．1.2倍にする場合は`1.2`． | 1.0 |
| kokoro_split_regex | 区切る文字 ．設定した文字で区切らせて発話できる．| r'[\n,.!?、。！？]+' |
| kokoro_device | 使用する計算デバイス (cpu or cuda:0)．空の場合，利用可能なGPUがあれば優先的に選択し，なければCPUが自動選択される．| '' |

<p align="right">(<a href="#kokoro-top">Kokoro TTSトップに戻る</a>)</p>


<a name="openpico-top"></a>

# OpenPico
OpenPicoは[OpenJTalk](https://open-jtalk.sourceforge.net/)と[SVOX Pico](https://www.openhab.org/addons/voice/picotts/)を組み合わせたものです．
OpenJTalkは日本語のテキストを音声に変換するためのオープンソースの音声合成ソフトウェアです．
SVOX Picoは様々な言語に対応した軽量なテキスト音声変換（TTS）エンジンです．


## インストール方法
1. sobits_ttsのinstallディレクトリに移動
    ```sh
    cd ~/colcon_ws/src/sobits_tts/install/
    ```

2. モデルをインストール
    ```bash
    bash openpico.sh
    ```

<p align="right">(<a href="#openpico-top">OpenPico TTSに戻る</a>)</p>

## 実行・操作方法
1. [openpico.launch.py](launch/openpico.launch.py)を起動
    ```bash
    ros2 launch sobits_tts openpico.launch.py
    ```

2. Action Clientを起動

<p align="right">(<a href="#openpico-top">OpenPico TTSに戻る</a>)</p>

## パラメータ
### 対応言語
OpenPicoは以下の言語に対応しています．\
[openpico.launch.py](launch/openpico.launch.py)の**openpico_language**を使用する言語に書き換えてください．

| 対応言語  | openpico_language |
| ----- | ----- |
| 英語 | en |
| 日本語 | ja |

<p align="right">(<a href="#openpico-top">OpenPico TTSに戻る</a>)</p>

### 話者
OpenPicoは日本語のみ様々な話者に対応しています．\
`install/openpico.sh` 実行時に Mei voice（CC-BY 3.0）が `/opt/mei_voice/` にダウンロードされます．\
[openpico.launch.py](launch/openpico.launch.py)の**openpico_voice_data_ja**を使用する話者のファイルパスに書き換えてください．

<p align="right">(<a href="#openpico-top">OpenPico TTSに戻る</a>)</p>

<a name="coqui-top"></a>

# Coqui TTS
[Coqui TTS](https://github.com/coqui-ai/TTS)は，テキストから音声を生成するためのオープンソースの音声合成ツールキットです．

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
    $ echo "alias tts_launch='docker run --rm -it -p 5002:5002 -v ~/{PATH_ROS_WS_LOCAL}/src/sobits_tts/install/coqui/models/:/root/.local/share/tts/ --entrypoint \"tts-server\" ghcr.io/coqui-ai/tts-cpu'" >> ~/.bash_aliases
    ```
    - **GPU**の場合:
    ```sh
    $ echo "alias tts_launch='docker run --rm -it -p 5002:5002 --gpus all -v ~/{PATH_ROS_WS_LOCAL}/src/sobits_tts/install/coqui/models/:/root/.local/share/tts/ --entrypoint \"tts-server\" ghcr.io/coqui-ai/tts'" >> ~/.bash_aliases
    ```
> [!IMPORTANT]
> `{PATH_ROS_WS_LOCAL}` は**ローカル環境**に存在するROSのワークスペースのPATHである．

> [!IMPORTANT]
> すでに，Dockerのコンテナーの中にいる場合，ローカル環境上でコマンド3を実行する必要がある．

<p align="right">(<a href="#coqui-top">Coqui TTSトップに戻る</a>)</p>

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

<p align="right">(<a href="#coqui-top">Coqui TTSトップに戻る</a>)</p>

## パラメータ
[coqui.launch.py](launch/coqui.launch.py)で以下のパラメータを指定できます．

| パラメータ  | パラメータ名 | 説明 | デフォルト値 |
| ----- | ----- | ----- | ----- |
| 対応言語 | coqui_language_id | 使用する言語のID (英語のみ) | |
| 話者 | coqui_speaker_id | 使用する話者のID (p225 ~ p376) | p225 |
| 句読点の自動追加 | coqui_add_stop_char | テキストの最後に句読点を自動追加するかどうか | True |

<p align="right">(<a href="#coqui-top">Coqui TTSトップに戻る</a>)</p>

<a name="parler-top"></a>

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

<p align="right">(<a href="#parler-top">Parler TTSトップに戻る</a>)</p>

## 実行・操作方法
1. [parler.launch.py](launch/parler.launch.py)を起動 (時間がかかるので注意)
    ```bash
    ros2 launch sobits_tts parler.launch.py
    ```

2. Action Clientを起動

<p align="right">(<a href="#parler-top">Parler TTSトップに戻る</a>)</p>

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

<p align="right">(<a href="#parler-top">Parler TTSトップに戻る</a>)</p>

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

<p align="right">(<a href="#parler-top">Parler TTSトップに戻る</a>)</p>

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

<p align="right">(<a href="#parler-top">Parler TTSトップに戻る</a>)</p>

## 発話させる文章について

- **文末にピリオド(.)あるいは句点(。)をつけてください．**
- **数字について，半角(1, 2など)より，one, 二などを推奨**
- 句読点は，世代の韻律を制御するために使用できます(たとえば，カンマを使用して音声に小さな区切りを追加します)
- 1単語のみ発話させる場合は生成に時間がかかります

<p align="right">(<a href="#parler-top">Parler TTSトップに戻る</a>)</p>

<a name="openaudio-top"></a>

# Open Audio TTS
Open Audio TTSはZero-shotやFew-shotでの音声クローン，多様な感情，トーン，特殊マーカーをサポートしています．**録音した声を再現し，好きな声で好きな文章を発話でさせることができます．**

VRAM8GB以上のGPUでの使用を推奨します．


Open Audio TTSは以下の言語に対応しています．言語は自動検出されるため設定する必要はありません．

| | | | |
| --- | --- | --- | --- |
| 英語 | 中国語 | 日本語 | ドイツ語 |
| フランス語 | スペイン語 | 韓国語 | アラビア語 |
| ロシア語 | オランダ語 | イタリア語 | ポーランド語 |
| ポルトガル語 |  |  |  |

<p align="right">(<a href="#openaudio-top">Open Audio TTSトップに戻る</a>)</p>

## インストール方法
1. [Hugging Face](https://huggingface.co/)のアカウント作成

    上記リンクへアクセスし，Sign UpからHugging Faceのアカウントを作成します．既にアカウントがある場合は2へ進みます．
2. [モデルページ](https://huggingface.co/fishaudio/openaudio-s1-mini)にアクセスし，規約を読んで同意します．
    下記のような文章がある箇所です．

    You need to agree to share your contact information to access this model.

3. Hugging Faceのアクセストークン作成

    [Hugging Faceの設定ページ](https://huggingface.co/settings/tokens)にアクセスします．
	「New token」をクリックし，以下のように設定します．
    - Token type: fine-grained
    - Token name: 任意の名前
    - User Permissions:
        - Repositories：Read access to contents of all public gated repos you can access
        - Inference: Make calls to Inference Providers
    
    設定後，「Create token」をクリックしてトークンを生成します．
4. ターミナルを開き，sobits_ttsのinstallディレクトリに移動します．
    ```sh
    cd ~/colcon_ws/src/sobits_tts/install/
    ```

5. 依存関係をインストール
    ```bash
    bash openaudio.sh
    ```

<p align="right">(<a href="#openaudio-top">Open Audio TTSトップに戻る</a>)</p>

## 実行・操作方法

主に3通りの使い方があります．

- 通常のTTSとして使う場合
- マイクで録音した音声をクローンして発話させる場合
- すでに用意したwavファイルをクローンして発話させる場合

### 通常のTTSとして使う場合
1. [openaudio.launch.py](launch/openaudio.launch.py)を起動する．
    ```sh
    ros2 launch sobits_tts openaudio.launch.py
    ```

2. Action Clientを起動．

<p align="right">(<a href="#openaudio-top">Open Audio TTSトップに戻る</a>)</p>

### マイクで録音した音声をクローンして発話させる場合
1. Ubuntuの設定で，サウンドの入力デバイスを使用するマイクに設定する．
2. ターミナルを開いてtestディレクトリに移動し，[recorder.py](/test/recorder.py)を実行して録音する．
    ```sh
    cd ~/colcon_ws/src/sobits_tts/test/
    python3 recorder.py
    ```

3. [openaudio.launch.py](launch/openaudio.launch.py)にある**reference_audio_path**を，soundfileディレクトリに生成された**record.wavの絶対パス**に書き換える．
4. [openaudio.launch.py](launch/openaudio.launch.py)を起動する．
    ```sh
    ros2 launch sobits_tts openaudio.launch.py
   ```
5. Action Clientを起動する．

<p align="right">(<a href="#openaudio-top">Open Audio TTSトップに戻る</a>)</p>

### すでに用意したwavファイルをクローンして発話させる場合
1. [openaudio.launch.py](launch/openaudio.launch.py)にある**reference_audio_path**を、用意した**wavファイルの絶対パス**に書き換える．
2. [openaudio.launch.py](launch/openaudio.launch.py)を起動する．
3. Action Clientを起動する．

## パラメータ
### 感情，トーン，発話速度のコントロール
発話させるテキストにタグを指定することで感情や発話速度，トーンを制御できます．詳細は[公式ページ](https://docs.fish.audio/emotion-control/tts-emotion-and-control-tags-user-guide)を参照してください．


感情タグは文の先頭に，トーンマーカーと特別なマーカーは任意の位置に配置できます．

例
```
感情タグの使用法: (Happy)How are you today?
トーンマーカー: Help! (shouting) Hey!
特別なマーカー:What! (laughing) Ha,ha,ha!
```

<details>
 <summary>設定可能なすべてのタグ</summary>

1. 感情マーカー (文頭にのみ配置可能)

    (angry) (sad) (disdainful) (excited) (surprised) (satisfied) (unhappy) (anxious) (hysterical) (delighted) (scared) (worried) (indifferent) (upset) (impatient) (nervous) (guilty) (scornful) (frustrated) (depressed) (panicked) (furious) (empathetic) (embarrassed) (reluctant) (disgusted) (keen) (moved) (proud) (relaxed) (grateful) (confident) (interested) (curious) (confused) (joyful) (disapproving) (negative) (denying) (astonished) (serious) (sarcastic) (conciliative) (comforting) (sincere) (sneering) (hesitating) (yielding) (painful) (awkward) (amused)
2. トーンマーカー(任意の位置に配置可能)

    (in a hurry tone) (shouting) (screaming) (whispering) (soft tone)
3. 特別なマーカー(任意の位置に配置可能)

    (laughing) (chuckling) (sobbing) (crying loudly) (sighing) (panting) (groaning) (crowd laughing) (background laughter) (audience laughing)
</details>

<p align="right">(<a href="#openaudio-top">Open Audio TTSトップに戻る</a>)</p>

### 音声クローンについて
以下のコマンドで，launch起動後でも参照音声を変更できます．**参照音声ファイルの絶対パス**を書き換えてください．
```sh
ros2 param set /tts_action_server openaudio_tts.reference_audio_path ${参照音声ファイルの絶対パス}
```
また，以下のコマンドでも同様に，launch起動後でも参照音声に対応するテキストを変更できます．
```sh
ros2 param set /tts_action_server openaudio_tts.reference_text ${参照音声に対応するテキスト}
```

以下に推奨する参照音声の条件について説明します．
詳細は[公式ページ](https://docs.fish.audio/text-to-speech/voice-clone-best-practices)を参照してください．

- 単一の話者のみ
- 安定した音量，トーン，感情
- 短い一時停止(0.5秒を推奨)
- 簡単な音声クローン作成
    - 30〜45秒の高品質オーディオ
    - ベスト: 完全な段落を形成する 2-3 個の 15-20 秒の音声
- 高品質な音声クローン作成
    - 30〜180分の高品質オーディオ
    - 複数の言語と感情
    - 背景雑音なし
    - 高い録音品質
    - 反響音なし

<p align="right">(<a href="#openaudio-top">Open Audio TTSトップに戻る</a>)</p>

## launchファイルで設定可能なパラメータ

以下は[openaudio.launch.py](launch/openaudio.launch.py)で設定可能なパラメータです．
 以下のコマンドでlaunch ファイル起動後もパラメーターを動的に変更可能です．

 例：音声クローンのための参照音声のファイルの絶対パスを変更する場合
```sh
ros2 param set /tts_action_server openaudio_tts.reference_audio_path
```


| パラメータ名                 | 説明                                | 変更の影響                                                       | デフォルト値         |
| --- | ---------- | ------------ | -------------- |
| `reference_audio_path` | 音声クローンのための参照音声のファイルの絶対パス            | 指定するとモデルがその音声のトーン・声質を学習し出力に反映                | `""`           |
| `reference_text`       | 参照音声で発話されているテキスト   | 設定すると精度が向上するが生成速度が遅くなる．        | `""`           |
| `reference_id`         | 参照データに付ける識別子                     | 複数の参照を使う際にIDで区別・管理可能．空の場合は識別なし．                             | `None`         |
| `seed`                 | 話者の再現性を確保するための乱数シード           | 指定すると常に同じ話者で発話する．0かNoneだと完全ランダムな話者で発話する．                              | `None`         |
| `use_memory_cache`     | 中間結果をメモリにキャッシュするかどうか                | キャッシュを有効にすると処理が高速化するが，メモリ使用量が増加する．                     | `False`         |
| `chunk_length`         | 推論時にテキストを分割する際の1チャンクの文字数         | 小さくすると応答開始が早くなるが，分割が細かくなり文脈つながりが損なわれる場合がある．大きくするとメモリ消費増．    | `200`          |
| `normalize`            | 出力波形の音量を一貫させる正規化を行うかどうか             | Falseにすると出力音声の音量にばらつきが出る．録音元の音量に依存したまま出力される．                 | `True`         |
| `max_new_tokens`       | 生成する新トークン数の上限                    | 上限を小さくすると短文出力や出力途中終了が多くなる．大きくすると処理時間・メモリ使用量が増える．     | `512`         |
| `top_p`                | 生成されるテキストの多様性と確実性を制御するカーネル サンプリング確率                 | 小さい値（例えば0.3）にすると出力の多様性が減り安定．大きいと多様性が増す．    | `0.65`          |
| `repetition_penalty`   | 同じフレーズの繰り返しを抑制する値        | 値が大きいほど同一表現の繰り返しが減るが，文の自然な連続性に悪影響を及ぼす可能性もある．                | `1.1`          |
| `temperature`          | 生成されるテキストのランダム性を調整する温度係数       | 0.2 など低い値に設定すると最も確率の高い語を機械的に選ぶためニュース読み上げのような安定した出力になる．0.9 以上に上げると珍しい語も採用してキャラクター性の強いセリフが出力される． | `0.8`          |

以下のパラメータはlaunch起動後に動的に変更不可能なものです．
||||
|---|---|---|
| `use_half_precision`   | 推論に半精度（FP16）を使用するかどうか                 | 速度とメモリ使用量が改善されるが，音質や安定性に微妙な劣化が出る場合がある                     | `True`         |
| `device`               | 使用する推論デバイス（`cuda` か `cpu`）       | `cpu` にするとGPUより遅くなるが，環境に依存せずどこでも動作する．`cuda`なら高速化・FP16も利用可能． | `cuda`         |
| `compile_model`        | `torch.compile()`によるモデル高速化を適用するか | 有効化で推論は高速化するが，初回ロード時にコンパイル時間がかかる．     | `False`        |
| `max_text_length`      | 入力テキストの最大文字数                     | この長さを超えると切り捨てて複数チャンクになるため，一貫した長文生成には注意が必要だが，処理負荷は抑えられる．     | `256`          |
| `listen_address`       | TTSサーバーがリクエストを受け付けるIPアドレス・ポート    | アドレスを変更するとサーバーが待機するネットワークインタフェースや接続可能範囲が変わる               | `0.0.0.0:8080` |

<p align="right">(<a href="#openaudio-top">Open Audio TTSトップに戻る</a>)</p>

<a name="voicevox-top"></a>

# Voicevox TTS

[Voicevox](https://github.com/VOICEVOX/voicevox_core?tab=readme-ov-file)は無料で使える中品質なテキスト読み上げ・歌声合成ソフトウェアです．対応言語は日本語のみです．英語を発話させたい場合はカタカナにすることで発話させることができます．

## インストール方法
1. sobits_ttsのinstallディレクトリに移動
    ```sh
    cd ~/colcon_ws/src/sobits_tts/install/
    ```

2. モデルをインストール．GPUを使用する場合は-gを末尾に追加.
    ```bash
    bash voicevox.sh
    ```

<p align="right">(<a href="#voicevox-top">Voicevox TTSトップに戻る</a>)</p>

## 実行・操作方法
1. [voicevox.launch.py](launch/voicevox.launch.py)を起動
    ```bash
    ros2 launch sobits_tts voicevox.launch.py
    ```

2. Action Clientを起動

<p align="right">(<a href="#voicevox-top">Voicevox TTSトップに戻る</a>)</p>

## パラメータ
[voicevox.launch.py](launch/voicevox.launch.py)で以下のパラメータを指定できます．
以下のコマンドでlaunch ファイル起動後もパラメーターを動的に変更可能です．

例：スタイルIDを1に変更する場合
```sh
ros2 param set /tts_action_server voicevox.style_id 1
```




| パラメータ | パラメータ名 | 説明 | デフォルト値 |
| --- |  --- |  --- |  --- | 
| スタイルID |  voicevox_style_id |  話し方を指定する．[VVMファイルとスタイルIDの対応表](https://github.com/VOICEVOX/voicevox_vvm/blob/main/README.md#%E9%9F%B3%E5%A3%B0%E3%83%A2%E3%83%87%E3%83%ABvvm%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%A8%E5%A3%B0%E3%82%AD%E3%83%A3%E3%83%A9%E3%82%AF%E3%82%BF%E3%83%BC%E3%82%B9%E3%82%BF%E3%82%A4%E3%83%AB%E5%90%8D%E3%81%A8%E3%82%B9%E3%82%BF%E3%82%A4%E3%83%AB-id-%E3%81%AE%E5%AF%BE%E5%BF%9C%E8%A1%A8)を参照すること． |  14 |
| VVMファイル名	 |  voicevox_model_file_num | 話者を指定する．上記の対応表を参照すること．|  1.vvm |
| 発話速度 | voicevox_speed_scale |  1.0 → 1.5 にすると発話速度が50%アップ．1.0 → 0.5にすると発話速度が50%ダウン． |  1.0 | 
| ピッチスケール |  voicevox_pitch_scale |  上げると高くなる．正の値（例：+1.0）を指定すると，声が高くなり可愛い印象．負の値（例：−1.0）では低い声に変化し，落ち着いた印象． |  0.0 | 
| イントネーション |  voicevox_intonation_scale |  値を 0に近づけると，平坦で単調な音声になる． |  1.0 | 
| 音量 |  voicevox_volume_scale |  1.0 → 2.0 にすると倍の音量になる．1.0 → 0.5 にすると半分の音量になる．|  1.0 | 
| 音声の前の無音時間 |  voicevox_pre_phoneme_length |  0.3にすると音声開始前に0.3秒の空白が入る． |  0.1 | 
| 音声の後の無音時間 |  voicevox_post_phoneme_length |  0.3にすると音声終了後に0.3秒の空白が入る． |  0.1 | 
| サンプリングレート |  voicevox_output_sampling_rate |  高くすると音質が向上する． |  48000 | 
| ステレオ出力 |  voicevox_output_stereo |  左右2つのスピーカーで音を分けて立体的に聞こえるように出力するかどうか． |  false | 

<p align="right">(<a href="#voicevox-top">Voicevox TTSトップに戻る</a>)</p>

<a name="supertonic-top"></a>

# Supertonic TTS
[Supertonic TTS](https://github.com/supertone-inc/supertonic)は極限の計算負荷で極限のパフォーマンスを目指した，非常に高速なオンデバイステキスト読み上げシステムです．ONNX Runtimeを搭載し，完全にデバイス上で動作します．Raspberry Pi上でも動作します．

## インストール方法
1. sobits_ttsのinstallディレクトリに移動
    ```sh
    cd ~/colcon_ws/src/sobits_tts/install/
    ```

2. モデルをインストール
    ```bash
    bash supertonic.sh
    ```

<p align="right">(<a href="#supertonic-top">Supertonic TTSトップに戻る</a>)</p>

## 実行・操作方法
1. [supertonic.launch.py](launch/supertonic.launch.py)を起動
    ```sh
    ros2 launch sobits_tts supertonic.launch.py
    ```

2. Action Clientを起動

<p align="right">(<a href="#supertonic-top">Supertonic TTSトップに戻る</a>)</p>

## パラメータ
[supertonic.launch.py](launch/supertonic.launch.py)で以下のパラメータを指定できます．

以下のコマンドでlaunch ファイル起動後もパラメーターを動的に変更可能です．

例：supertonic.voice_nameをM1に変更する場合
```sh
ros2 param set /tts_action_server supertonic.voice_name M1
```


| パラメータ名 | 説明 | デフォルト値 |
| --- | --- | --- |
| supertonic_device | 使用する計算デバイス (cpu or cuda)．空の場合，利用可能なGPUがあれば優先的に選択し，なければCPUが自動選択される． | 'cpu' |
| supertonic_voice_name | 話者．M1, M2, M3, M4, M5, F1, F2, F3, F4, F5から選択可能． | 'F1' |
| supertonic_language | 言語．`en`, `ko`, `es`, `pt`, `fr`から選択可能． | 'en' |
| supertonic_total_steps | ノイズ除去ステップ数．高くすると音質が良くなるが生成時間が遅くなる．| 5 |
| supertonic_speed | 発話する速度．1.2倍にする場合は`1.2`．上げると読み飛ばしが起こりやすくなる． | 1.05 |
| supertonic_max_chunk_length | 一度に処理するテキストの最大文字数．| 300 |
| supertonic_silence_duration | 文と文の間に挿入する無音時間（秒数）．| 0.3 |

言語は英語，韓国語，スペイン語，ポルトガル語，フランス語に対応しています．

<p align="right">(<a href="#supertonic-top">Supertonic TTSトップに戻る</a>)</p>

<a name="piper-top"></a>

# Piper TTS
[Piper TTS](https://github.com/OHF-Voice/piper1-gpl)は音声化のために[espeak-ng](https://github.com/espeak-ng/espeak-ng)を埋め込む高速かつローカルなニューラルテキスト読み上げエンジンです．

<p align="right">(<a href="#piper-top">Piper TTSトップに戻る</a>)</p>

## インストール方法
1. sobits_ttsのinstallディレクトリに移動
    ```sh
    cd ~/colcon_ws/src/sobits_tts/install/
    ```

2. モデルをインストール
    ```bash
    bash piper.sh
    ```
<p align="right">(<a href="#piper-top">Piper TTSトップに戻る</a>)</p>

## 実行・操作方法
1. [piper.launch.py](launch/piper.launch.py)を起動
    ```sh
    ros2 launch sobits_tts piper.launch.py
    ```

2. Action Clientを起動

<p align="right">(<a href="#piper-top">Piper TTSトップに戻る</a>)</p>

## パラメータ
[piper.launch.py](launch/piper.launch.py)で以下のパラメータを指定できます．

以下のコマンドでlaunch ファイル起動後もパラメーターを動的に変更可能です．

例：piper.volumeを5.0に変更する場合
```sh
ros2 param set /tts_action_server piper.volume 5.0
```

| パラメータ名 | 説明 | デフォルト値 |
| --- | --- | --- |
| piper_model | 使用するモデル名．なければ自動ダウンロードされる． | en_US-lessac-medium |
| piper_length_scale | 話速の倍率．1.0 より小さいと速く、1.0 より大きいと遅くなる． | 1.0 |
| piper_noise_scale | 音声の揺らぎ（感情の起伏）．値を変えると声の質感や抑揚が変化する． | 0.667 |
| piper_noise_w_scale | 音素の長さのばらつき（抑揚）．発音のタイミングのランダム性を制御する． | 0.8 |
| piper_volume | 音量の倍率． | 1.0 |
| piper_speaker_id | マルチスピーカーモデルの話者ID． | 0 |

- ダウンロード可能なモデル一覧は以下のコマンドで確認できます
    ```sh
    python3 -m piper.download_voices
    ```
- ダウンロード済みモデルは以下のコマンドで確認できます
    ```sh
    ls ~/.sobits_tts/piper/*.onnx | xargs -n 1 basename | sed 's/\.onnx//'
    ```
- モデルの音声サンプルは[こちら](https://rhasspy.github.io/piper-samples/)で確認できます．


<p align="right">(<a href="#piper-top">Piper TTSトップに戻る</a>)</p>

<p align="right">(<a href="#readme-top">ページトップに戻る</a>)</p>