#!/bin/bash

echo "╔══╣ Install: Coqui TTS (STARTING) ╠══╗"

sudo apt-get update -y 

sudo apt install ffmpeg

python3 -m pip install -U pip --break-system-packages
python3 -m pip install \
    requests --break-system-packages

echo "╚══╣ Install: Coqui TTS (FINISHED) ╠══╝"