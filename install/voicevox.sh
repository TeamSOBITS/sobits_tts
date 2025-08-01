#!/bin/bash
echo "╔══╣ Install: voicevox TTS (STARTING) ╠══╗"

while getopts "cg" opt; do
  case $opt in
    c) USE_CPU=true ;; 
    g) USE_GPU=true ;;  
    *) echo "Usage: $0 [-c for CPU version] [-g for GPU version]" ;;
  esac
done

if [ -z "$USE_CPU" ] && [ -z "$USE_GPU" ]; then
  echo "Please specify either -c for CPU or -g for GPU."
  USE_CPU=true
fi

sudo apt update -y

echo "Download downloder"
wget https://github.com/VOICEVOX/voicevox_core/releases/download/0.16.0/download-linux-x64

chmod +x download-linux-x64

echo
if [ "$USE_GPU" == "true" ]; then
    echo "Installing GPU version..."
    ./download-linux-x64 --exclude c-api --devices cuda 
elif [ "$USE_CPU" == "true" ]; then
    echo "Installing CPU version..."
    ./download-linux-x64 --exclude c-api 
fi

echo "Install whl"
pip3 install https://github.com/VOICEVOX/voicevox_core/releases/download/0.16.0/voicevox_core-0.16.0-cp310-abi3-manylinux_2_34_x86_64.whl

echo "╚══╣ Install: voicevox TTS (FINISHED) ╠══╝"
