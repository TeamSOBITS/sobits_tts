#!/bin/bash
set -e

REAL_USER=${SUDO_USER:-$(whoami)}
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
IRODORI_DIR="$SCRIPT_DIR/irodori/Irodori-TTS"
IRODORI_COMMIT="89f9d8fbd4d51ea019867ee1197725ede1df13c5"

echo "╔══╣ Install: Irodori TTS (STARTING) ╠══╗"

while getopts "cg" opt; do
  case $opt in
    c) USE_CPU=true ;;
    g) USE_GPU=true ;;
    *) echo "Usage: $0 [-c for CPU version] [-g for GPU version]" ;;
  esac
done

if [ -z "$USE_CPU" ] && [ -z "$USE_GPU" ]; then
  echo "Neither -c nor -g was specified. Installing GPU version (CUDA 12.8)."
  USE_GPU=true
fi

# Irodori TTS needs transformers 5 and torch 2.10, which conflict with other TTS (e.g. Kokoro needs transformers 4.37).
# It is installed into its own venv under install/irodori/ and does not touch the system Python packages.
pip3 install uv --break-system-packages

echo "[Irodori] Cloning Irodori-TTS..."
if [ ! -d "$IRODORI_DIR" ]; then
    git clone https://github.com/Aratako/Irodori-TTS.git "$IRODORI_DIR"
fi
git -C "$IRODORI_DIR" fetch origin
git -C "$IRODORI_DIR" checkout "$IRODORI_COMMIT"

echo "[Irodori] Creating venv and installing dependencies..."
cd "$IRODORI_DIR"
if [ "$USE_GPU" == "true" ]; then
    python3 -m uv sync --extra cu128
else
    python3 -m uv sync --extra cpu
fi

echo "[Irodori] Pre-downloading models for offline use..."
sudo -H -u "$REAL_USER" "$IRODORI_DIR/.venv/bin/python" -c "
from huggingface_hub import snapshot_download
snapshot_download('Aratako/Irodori-TTS-v4.1-Small', allow_patterns=['model.safetensors', 'tokenizer/*'])
snapshot_download('Aratako/Semantic-DACVAE-Japanese-32dim')
snapshot_download('sony/silentcipher')
"

echo "╚══╣ Install: Irodori TTS (FINISHED) ╠══╝"
