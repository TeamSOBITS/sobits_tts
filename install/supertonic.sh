#!/bin/bash
set -e

REAL_USER=${SUDO_USER:-$(whoami)}

echo "╔══╣ Install: Supertonic TTS (STARTING) ╠══╗"

pip3 install supertonic soundfile scipy --break-system-packages
pip3 install "numpy>=1.26.0,<2.0.0" --force-reinstall --break-system-packages

echo "[Supertonic] Setting up onnxruntime (CPU)..."
pip3 uninstall -y onnxruntime-gpu --break-system-packages
pip3 install onnxruntime --break-system-packages

echo "[Supertonic] Pre-downloading Supertonic-3 model for offline use..."
sudo -H -u "$REAL_USER" python3 -c "from supertonic import TTS; TTS(model='supertonic-3', auto_download=True)"

echo "╚══╣ Install: Supertonic TTS (FINISHED) ╠══╝"
