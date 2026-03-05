#!/bin/bash
echo "╔══╣ Install: Kokoro TTS (STARTING) ╠══╗"

export PIP_BREAK_SYSTEM_PACKAGES=1

sudo apt update -y

sudo apt install -y espeak-ng

pip3 install -q kokoro==0.9.4 --break-system-packages
pip3 install -q 'misaki[en,ja]==0.9.4' --break-system-packages

pip3 uninstall -y fugashi unidic unidic-lite --break-system-packages
pip3 install -q fugashi unidic-lite --break-system-packages

pip3 install transformers==4.37.2 --break-system-packages

pip3 install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl --break-system-packages

echo "╚══╣ Install: Kokoro TTS (FINISHED) ╠══╝"
