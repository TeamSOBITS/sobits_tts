#!/bin/bash

echo "╔══╣ Install: Supertonic TTS (STARTING) ╠══╗"

sudo apt-get update -y 
sudo apt-get install -y git-lfs

echo "[Supertonic] Installing Python dependencies..."
pip3 install supertonic soundfile scipy
pip3 install "numpy>=1.26.0,<2.0.0" --force-reinstall

SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd "$SCRIPT_DIR"

if [ ! -d "supertonic" ]; then
    echo "[Supertonic] Cloning model repository..."
    git lfs install
    git clone https://huggingface.co/Supertone/supertonic
else
    echo "[Supertonic] Model directory already exists. Skipping clone."
    cd supertonic && git lfs pull && cd ..
fi


if command -v nvidia-smi &> /dev/null; then
    echo "[Supertonic] GPU detected. Installing onnxruntime-gpu..."
    pip3 uninstall -y onnxruntime onnxruntime-gpu
    pip3 install onnxruntime-gpu
else
    echo "[Supertonic] No GPU detected. Ensuring onnxruntime (CPU) is installed..."
    pip3 install onnxruntime
fi

echo "[Supertonic] Verifying NumPy version..."
python3 -c "import numpy; print(f'Installed NumPy: {numpy.__version__}')"

echo "╚══╣ Install: Supertonic TTS (FINISHED) ╠══╝"