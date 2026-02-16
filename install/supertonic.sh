#!/bin/bash

INSTALL_PATH="/opt/supertonic_model"
LINK_PATH="/opt/supertonic"
MODEL_REPO="https://huggingface.co/Supertone/supertonic-2"

REAL_USER=${SUDO_USER:-$USER}

echo "╔══╣ Install: Supertonic TTS (STARTING) ╠══╗"

sudo apt-get update -y 
sudo apt-get install -y git-lfs
pip3 install supertonic soundfile scipy --break-system-packages
pip3 install "numpy>=1.26.0,<2.0.0" --force-reinstall --break-system-packages

if [ -d "$INSTALL_PATH" ]; then
    sudo rm -rf "$INSTALL_PATH"
fi
sudo mkdir -p "$INSTALL_PATH"
sudo chmod 777 "$INSTALL_PATH"

echo "[Supertonic] Cloning Supertonic-2 model repository..."
git lfs install
git clone "$MODEL_REPO" "$INSTALL_PATH"

echo "[Supertonic] Setting correct permissions..."
sudo chown -R "$REAL_USER":"$REAL_USER" "$INSTALL_PATH"
sudo chmod 755 "$INSTALL_PATH"

sudo ln -sfn "$INSTALL_PATH" "$LINK_PATH"

# 6. GPU/CPU 設定
if command -v nvidia-smi &> /dev/null; then
    echo "[Supertonic] GPU detected. Setting up onnxruntime-gpu..."
    pip3 uninstall -y onnxruntime onnxruntime-gpu --break-system-packages
    pip3 install onnxruntime-gpu --break-system-packages
else
    echo "[Supertonic] No GPU detected. Setting up onnxruntime..."
    pip3 install onnxruntime --break-system-packages
fi

echo "╚══╣ Install: Supertonic TTS (FINISHED) ╠══╝"