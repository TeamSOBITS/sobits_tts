#!/bin/bash

echo "╔══╣ Install: SOBITS TTS (STARTING) ╠══╗"

sudo apt update -y

sudo apt install pulseaudio pulseaudio-utils -y

sudo apt install -y ros-${ROS_DISTRO}-vision-msgs

# Install "sobits_msgs"
cd ~/colcon_ws/src/
if [ ! -d "sobits_msgs" ]; then
    git clone -b ${ROS_DISTRO}-devel https://github.com/TeamSOBITS/sobits_msgs.git
else
    echo "sobits_msgs リポジトリはすでに存在します。スキップします。"
fi

pip3 install soundfile

pip3 install pygame

echo "╚══╣ Install: SOBITS TTS (FINISHED) ╠══╝"

