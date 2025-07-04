#!/bin/bash

echo "╔══╣ Install: Coqui TTS (STARTING) ╠══╗"

sudo apt-get update -y 

sudo apt install ffmpeg

python3 -m pip install -U pip
python3 -m pip install \
    requests \
    wave

echo "╚══╣ Install: Coqui TTS (FINISHED) ╠══╝"