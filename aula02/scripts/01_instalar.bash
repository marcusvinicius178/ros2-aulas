#!/usr/bin/env bash
# Executar como usuario normal; sudo sera solicitado somente pelo apt.
set -eo pipefail
source /etc/os-release
if [[ "${ID:-}" != ubuntu || "${VERSION_ID:-}" != 24.04 ]]; then
    echo 'Este roteiro exige Ubuntu 24.04. Nao instalara Jazzy em outra versao.' >&2
    exit 1
fi
if [[ ! -f /opt/ros/jazzy/setup.bash ]]; then
    echo 'Instale primeiro ROS 2 Jazzy Desktop pela Aula 01; depois repita.' >&2
    exit 1
fi
sudo apt update
sudo apt install \
    build-essential python3-colcon-common-extensions python3-yaml \
    ros-jazzy-navigation2 ros-jazzy-nav2-bringup \
    ros-jazzy-nav2-minimal-tb3-sim \
    ros-jazzy-turtlebot3-gazebo ros-jazzy-turtlebot3-description \
    ros-jazzy-cartographer-ros ros-jazzy-teleop-twist-keyboard \
    ros-jazzy-rviz2 ros-jazzy-tf2-ros-py ros-jazzy-rosidl-default-generators
printf '\nInstalacao concluida. Nao foi executado apt upgrade nem alterado o .bashrc.\n'
