#!/bin/bash
echo "╔══╣ Install: Open Audio TTS (STARTING) ╠══╗"

sudo apt update -y

sudo apt install portaudio19-dev python3-pyaudio -y

sudo apt install pulseaudio-utils -y

pip3 install torch torchaudio numpy scipy

pip3 install huggingface_hub
echo "export PATH=\"$(python3 -m site --user-base)/bin:\$PATH\"" >> ~/.bashrc

echo "╚══╣ Enter the created token to log in ╠══╝"
huggingface-cli login

echo "╚══╣ Starting model download ╠══╝"
huggingface-cli download fishaudio/openaudio-s1-mini --local-dir checkpoints/openaudio-s1-mini

pip3 install git+https://github.com/fishaudio/fish-speech.git

echo "╚══╣ Install: Open Audio TTS (FINISHED) ╠══╝"