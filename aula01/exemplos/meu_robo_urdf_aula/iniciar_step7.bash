#!/usr/bin/env bash
# Inicia SOMENTE a visualização do Step 7. Não compila nem altera outros passos.
set -e -o pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

if [[ -n "${ROS_DISTRO:-}" && -f "/opt/ros/${ROS_DISTRO}/setup.bash" ]]; then
    source "/opt/ros/${ROS_DISTRO}/setup.bash"
elif [[ -f /opt/ros/jazzy/setup.bash ]]; then
    source /opt/ros/jazzy/setup.bash
elif [[ -f /opt/ros/humble/setup.bash ]]; then
    source /opt/ros/humble/setup.bash
fi

if ! command -v ros2 >/dev/null 2>&1; then
    echo "ROS 2 não encontrado. Carregue a instalação utilizada na aula e tente novamente." >&2
    exit 1
fi
missing=()
for package in robot_state_publisher joint_state_publisher_gui rviz2; do
    if ! ros2 pkg prefix "$package" >/dev/null 2>&1; then
        missing+=("$package")
    fi
done
if (( ${#missing[@]} )); then
    printf 'Pacotes ROS ausentes: %s\n' "${missing[*]}" >&2
    if [[ "${ROS_DISTRO:-}" == jazzy || "${ROS_DISTRO:-}" == humble ]]; then
        echo "Instale antes da aula:" >&2
        echo "sudo apt update && sudo apt install ros-${ROS_DISTRO}-robot-state-publisher ros-${ROS_DISTRO}-joint-state-publisher-gui ros-${ROS_DISTRO}-rviz2" >&2
    fi
    exit 1
fi
if [[ -z "${DISPLAY:-}" && -z "${WAYLAND_DISPLAY:-}" ]]; then
    echo "Sessão gráfica não encontrada. Execute em um terminal do desktop, não em SSH sem interface gráfica." >&2
    exit 1
fi
python3 "$ROOT/validar_step7.py"
if command -v check_urdf >/dev/null 2>&1; then
    check_urdf "$ROOT/urdf/simple_robot_step7.urdf"
fi
printf '\nAbra os sliders: ombros, left_finger_joint e right_wrist_joint.\n'
printf 'O outro dedo acompanha por mimic. Ctrl+C encerra esta demonstração.\n\n'
exec ros2 launch "$ROOT/launch/display_step7.launch.py"
