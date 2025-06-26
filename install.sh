#!/bin/bash

echo "╔══╣ Install: sobits_tts Common Dependencies (STARTING) ╠══╗"

# システムのパッケージリストを更新
sudo apt update -y

sudo apt install -y ros-humble-vision-msgs

echo "--- Installing Common APT Dependencies ---"
# サウンド再生に必要なALSAユーティリティ
sudo apt install -y \
    alsa-utils

echo "--- Installing Common Python Dependencies ---"
# WAVファイルの読み書きに必要
pip3 install soundfile
# 音声再生に必要 (TTSアクションサーバーが使用)
pip3 install pygame

echo "--- Cloning Common ROS Dependencies ---"
# このスクリプトは ~/colcon_ws/src/sobits_tts/ の一つ上の階層 (sobits_ttsのあるディレクトリ) で実行されることを想定
cd ~/colcon_ws/src/ || { echo "Error: ~/colcon_ws/src/ not found. Please run this script from your workspace source directory."; exit 1; }

if [ ! -d "sobits_msgs" ]; then
    echo "Cloning sobits_msgs..."
    git clone -b ${ROS_DISTRO}-devel https://github.com/TeamSOBITS/sobits_msgs.git
else
    echo "sobits_msgs already exists. Skipping clone."
fi

# sobits_interfaces が sobits_msgs に含まれていない、または別途必要な場合
# if [ ! -d "sobits_interfaces" ]; then
#     echo "Cloning sobits_interfaces..."
#     git clone -b ${ROS_DISTRO}-devel https://github.com/TeamSOBITS/sobits_interfaces.git
# else
#     echo "sobits_interfaces already exists. Skipping clone."
# fi

echo "╚══╣ Install: sobits_tts Common Dependencies (FINISHED) ╠══╝"