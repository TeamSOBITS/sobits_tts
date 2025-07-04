#!/bin/bash
echo "╔══╣ Install: Kokoro TTS (STARTING) ╠══╗"

sudo apt update -y

sudo apt install -y espeak-ng

pip3 install -q kokoro==0.9.4
pip3 install -q 'misaki[en,ja]==0.9.4'

pip3 uninstall -y fugashi unidic unidic-lite
pip3 install -q fugashi unidic-lite

echo "╚══╣ Install: Kokoro TTS (FINISHED) ╠══╝"