#!/bin/bash

echo "╔══╣ Install: Parler TTS (STARTING) ╠══╗"

sudo apt update -y

pip3 install numpy==1.23.5

pip3 install git+https://github.com/getuka/RubyInserter.git

pip3 install parler_tts==0.2.3

pip3 uninstall -y torch torchvision torchaudio

pip3 install torch torchvision torchaudio

pip3 install transformers==4.46.1

echo "╚══╣ Install: Parler TTS (FINISHED) ╠══╝"