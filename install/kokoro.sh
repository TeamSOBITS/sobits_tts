#!/bin/bash
echo "╔══╣ Install: Kokoro TTS (STARTING) ╠══╗"

sudo apt update -y

sudo apt install -y espeak-ng

pip3 install -q kokoro==0.9.4 --break-system-packages
pip3 install -q 'misaki[en,ja]==0.9.4' --break-system-packages

pip3 uninstall -y fugashi unidic unidic-lite --break-system-packages
pip3 install -q fugashi unidic-lite --break-system-packages

pip3 install transformers==4.37.2

echo "╚══╣ Install: Kokoro TTS (FINISHED) ╠══╝"
