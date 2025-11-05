#! /bin/bash

echo "╔══╣ Install: OpenPico TTS (STARTING) ╠══╗"

sudo apt update -y

echo "Install gTTS"
python3 -m pip install gTTS==2.0.1 --break-system-packages
python3 -m pip install gTTS-token --upgrade --break-system-packages

echo "Install mpg321"
sudo apt install -y mpg321

echo "Install voice data"
sudo apt install -y \
    open-jtalk \
    open-jtalk-mecab-naist-jdic \
    hts-voice-nitech-jp-atr503-m001

echo "Install mutagen"
python3 -m pip install mutagen --break-system-packages

echo "Install pico2wave"
sudo apt install -y libttspico-utils

echo "Install alsa"
sudo apt install -y \
    alsa \
    alsa-utils

echo "╚══╣ Install: OpenPico TTS (FINISHED) ╠══╝"