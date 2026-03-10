#! /bin/bash

# HTS Voice "Mei" is included in this script's download step.
# Copyright (c) 2009-2018 Nagoya Institute of Technology, Department of Computer Science
# Released by MMDAgent Project Team: http://www.mmdagent.jp/
# License: Creative Commons Attribution 3.0 (CC-BY 3.0)
# See: https://creativecommons.org/licenses/by/3.0/

echo "╔══╣ Install: OpenPico TTS (STARTING) ╠══╗"

sudo apt update -y

echo "Install gTTS"
python3 -m pip install gTTS==2.0.1 --break-system-packages
python3 -m pip install gTTS-token --upgrade --break-system-packages

echo "Install mpg321"
sudo apt install -y mpg321

echo "Install voice data"
sudo apt install -y \
    open-jtalk \
    open-jtalk-mecab-naist-jdic \
    hts-voice-nitech-jp-atr503-m001

echo "Install mutagen"
python3 -m pip install mutagen --break-system-packages

echo "Install pico2wave"
sudo apt install -y libttspico-utils

echo "Install alsa"
sudo apt install -y \
    alsa \
    alsa-utils

echo "Download Mei voice (CC-BY 3.0, Nagoya Institute of Technology)"
MEI_VOICE_PATH="/opt/mei_voice"
sudo mkdir -p "$MEI_VOICE_PATH"
sudo chmod 777 "$MEI_VOICE_PATH"
python3 - <<PYEOF
import urllib.request, zipfile, io, os, sys

url = "https://master.dl.sourceforge.net/project/mmdagent/MMDAgent_Example/MMDAgent_Example-1.8/MMDAgent_Example-1.8.zip?viasf=1"
install_path = "/opt/mei_voice"

print("Downloading MMDAgent_Example-1.8.zip (~30MB)...")
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
except Exception as e:
    print(f"ERROR: Download failed: {e}", file=sys.stderr)
    sys.exit(1)

z = zipfile.ZipFile(io.BytesIO(data))
for name in z.namelist():
    if name.startswith("MMDAgent_Example-1.8/Voice/mei/") and name.endswith(".htsvoice"):
        basename = os.path.basename(name)
        dest = os.path.join(install_path, basename)
        with open(dest, "wb") as f:
            f.write(z.read(name))
        print(f"  -> {dest}")

print("Done.")
PYEOF
sudo chmod 755 "$MEI_VOICE_PATH"

echo "╚══╣ Install: OpenPico TTS (FINISHED) ╠══╝"