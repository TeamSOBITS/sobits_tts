#!/bin/bash

echo "╔══╣ Install: Open JTalk & Pico TTS Dependencies (STARTING) ╠══╗"

# システムのパッケージリストを更新 (念のためここでも実行)
sudo apt update -y

echo "--- Installing Open JTalk Dependencies ---"
# Open JTalk 本体
sudo apt install -y \
    open-jtalk \
    open-jtalk-mecab-naist-jdic \
    hts-voice-nitech-jp-atr503-m001

echo "--- Installing Pico TTS Dependencies ---"
# Pico TTS 本体 (pico2wave コマンドを含む)
sudo apt install -y \
    libttspico-utils

echo "╚══╣ Install: Open JTalk & Pico TTS Dependencies (FINISHED) ╠══╝"