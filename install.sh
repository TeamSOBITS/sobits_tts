#!/bin/bash

echo "╔══╣ Install: SOBITS TTS (STARTING) ╠══╗"

sudo apt update -y

sudo apt install pulseaudio pulseaudio-utils -y

sudo apt install -y ros-${ROS_DISTRO}-vision-msgs

# Install "sobits_interfaces"
cd ../
if [ ! -d "sobits_interfaces" ]; then
    git clone -b ${ROS_DISTRO}-devel https://github.com/TeamSOBITS/sobits_interfaces.git
    cd sobbits_interfaces/
    bash install.sh
    cd ..
else
    echo "sobits_interfaces リポジトリはすでに存在します。スキップします。"
fi

pip3 install soundfile --break-system-packages

pip3 install pygame --break-system-packages

echo "╚══╣ Install: SOBITS TTS (FINISHED) ╠══╝"
