# Use source, nao bash: source ~/ros2-aulas-aula02/aula02/scripts/ambiente.bash
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    echo 'Use: source /caminho/ros2-aulas/aula02/scripts/ambiente.bash' >&2
    exit 1
fi
if [[ -n "${CONDA_PREFIX:-}" || -n "${VIRTUAL_ENV:-}" ]]; then
    echo 'Desative Conda/venv antes de carregar o ROS do sistema.' >&2
    return 1
fi
if [[ -n "${ROS_DISTRO:-}" && "$ROS_DISTRO" != jazzy ]]; then
    echo "Este terminal tem ROS_DISTRO=$ROS_DISTRO. Use um terminal sem outra distribuicao ROS." >&2
    return 1
fi
if [[ ! -f /opt/ros/jazzy/setup.bash ]]; then
    echo 'ROS 2 Jazzy nao encontrado em /opt/ros/jazzy.' >&2
    return 1
fi
# Scripts de setup do ROS podem acessar variaveis indefinidas: nao usar nounset durante source.
_aula02_had_u=0
case $- in *u*) _aula02_had_u=1; set +u ;; esac
source /opt/ros/jazzy/setup.bash
export AULA02_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export AULA02_WS="$HOME/ros2_aula02_ws"
export AULA02_DATA="$HOME/ros2_aula02_dados"
export ROS_DOMAIN_ID="${ROS_DOMAIN_ID:-42}"
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export TURTLEBOT3_MODEL=waffle
if [[ -f "$AULA02_WS/install/local_setup.bash" ]]; then
    source "$AULA02_WS/install/local_setup.bash"
fi
if [[ "$_aula02_had_u" == 1 ]]; then set -u; fi
unset _aula02_had_u
