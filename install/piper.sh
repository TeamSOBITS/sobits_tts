#!/usr/bin/env bash

set -e

echo "========================================"
echo " Installing Piper TTS"
echo "========================================"

echo "[1/3] Installing piper..."
pip3 install --upgrade piper
MODEL_DIR="$HOME/.sobits_tts/piper"
mkdir -p "$MODEL_DIR"


echo "[2/3] Model directory: $MODEL_DIR"
MODELS=(
    "en_US-lessac-medium"
    "en_US-amy-medium"
)


echo "[3/3] Installing default models..."
for MODEL in "${MODELS[@]}"; do
    if [ -f "$MODEL_DIR/$MODEL.onnx" ]; then
        echo "  - $MODEL already exists. Skipping."
    else
        echo "  - Downloading $MODEL ..."
        python3 -m piper.download_voices "$MODEL" --download-dir "$MODEL_DIR"
        echo "    Done."
    fi
done

echo "========================================"
echo " Piper installation completed."
echo "========================================"
