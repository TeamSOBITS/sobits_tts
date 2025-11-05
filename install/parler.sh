#!/bin/bash

echo "╔══╣ Install: Parler TTS (STARTING) ╠══╗"

sudo apt update -y

pip3 install numpy==1.23.5 --break-system-packages

pip3 install git+https://github.com/getuka/RubyInserter.git --break-system-packages

pip3 install parler_tts==0.2.3 --break-system-packages

pip3 uninstall -y torch torchvision torchaudio --break-system-packages

pip3 install torch torchvision torchaudio --break-system-packages

pip3 install transformers==4.46.1 --break-system-packages

echo "╚══╣ Install: Parler TTS (FINISHED) ╠══╝"