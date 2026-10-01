#!/usr/bin/env bash
# Somente leitura. Nao instala pacotes e nao publica comandos de movimento.
set -eo pipefail
printf '\n=== Sistema ===\n'
cat /etc/os-release
printf '\n=== Arquitetura / kernel ===\n'
uname -m
uname -r
printf '\n=== Ambiente recebido ===\n'
printf 'ROS_DISTRO=%s\nCONDA_PREFIX=%s\nVIRTUAL_ENV=%s\nAMENT_PREFIX_PATH=%s\n' \
    "${ROS_DISTRO:-}" "${CONDA_PREFIX:-}" "${VIRTUAL_ENV:-}" "${AMENT_PREFIX_PATH:-}"
printf '\n=== Pacotes instalados ===\n'
dpkg-query -W -f='${Package} ${Version}\n' \
    ros-jazzy-desktop ros-jazzy-nav2-bringup ros-jazzy-navigation2 \
    ros-jazzy-turtlebot3-gazebo ros-jazzy-nav2-minimal-tb3-sim \
    ros-jazzy-cartographer-ros ros-jazzy-ros-gz-sim \
    ros-jazzy-teleop-twist-keyboard 2>/dev/null || true
if [[ ! -f /opt/ros/jazzy/setup.bash ]]; then
    echo 'FALHA: falta /opt/ros/jazzy/setup.bash'; exit 1
fi
source /opt/ros/jazzy/setup.bash
printf '\n=== Launch e tipo de velocidade instalados ===\n'
share="$(ros2 pkg prefix --share turtlebot3_gazebo 2>/dev/null || true)"
if [[ -n "$share" ]]; then
    grep -nE 'ros_gz_sim|gzserver|GZ_SIM_RESOURCE_PATH' "$share/launch/turtlebot3_world.launch.py" || true
    grep -n -A4 'ros_topic_name:.*cmd_vel' "$share/params/turtlebot3_waffle_bridge.yaml" || true
fi
printf '\n=== Python do sistema / rclpy ===\n'
/usr/bin/python3 -c 'import sys, rclpy; print(sys.version); print(rclpy.__file__)'
printf '\nDiagnostico concluido; este teste nao comprova que a simulacao funciona.\n'
