#!/bin/bash

echo "╔══╣ Install: Kokoro TTS Dependencies (STARTING) ╠══╗"

# システムのパッケージリストを更新 (念のためここでも実行)
sudo apt update -y

echo "--- Installing Kokoro Python Dependencies ---"
# Kokoro TTS Pythonライブラリ
# バージョンは利用可能なものに合わせて調整してください
pip3 install kokoro
pip3 install misaki[en,ja]

sudo apt install -y espeak-ng

echo "╚══╣ Install: Kokoro TTS Dependencies (FINISHED) ╠══╝"