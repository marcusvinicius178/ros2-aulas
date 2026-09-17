set -euo pipefail
 
# Runs the osrf/car_demo Docker image built by ./build_demo.bash
#
# Usage:
#   ./run_demo.bash
#   ./run_demo.bash --nvidia
#
# Notes for hybrid Intel+NVIDIA laptops:
# - Mapping /dev/dri avoids "MESA-LOADER: failed to retrieve device information"
# - Forcing GLX vendor to NVIDIA avoids Gazebo/RViz picking Mesa/Intel by accident
 
IMAGE_NAME="osrf/car_demo"
USE_NVIDIA="false"
 
# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --nvidia)
      USE_NVIDIA="true"
      shift
      ;;
    -h|--help)
      echo "Usage: $0 [--nvidia]"
      exit 0
      ;;
    *)
      echo "Ignoring unknown argument: $1"
      shift
      ;;
  esac
done
 
if ! command -v docker >/dev/null 2>&1; then
  echo "docker not found. Install Docker first."
  exit 1
fi
 
if [[ -z "${DISPLAY:-}" ]]; then
  echo "DISPLAY is empty. Start an X11 session first."
  exit 1
fi
 
# Check image exists
if ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
  echo "Docker image ${IMAGE_NAME} not found."
  echo "Build it first with: ./build_demo.bash"
  exit 1
fi
 
# Allow local root to access X (simplest approach)
if command -v xhost >/dev/null 2>&1; then
  xhost +local:root >/dev/null 2>&1 || true
else
  echo "xhost not found. Install with: sudo apt install -y x11-xserver-utils"
  exit 1
fi
 
DOCKER_ARGS=(
  --rm
  -it
  --net=host
  --ipc=host
  -e "DISPLAY=${DISPLAY}"
  -e "QT_X11_NO_MITSHM=1"
  -v "/tmp/.X11-unix:/tmp/.X11-unix:rw"
)
 
# Pass joystick devices if present
if [[ -e /dev/input/js0 ]]; then
  DOCKER_ARGS+=(--device=/dev/input/js0:/dev/input/js0)
fi
if [[ -e /dev/input/js1 ]]; then
  DOCKER_ARGS+=(--device=/dev/input/js1:/dev/input/js1)
fi
 
# Map DRM devices to fix Mesa / device info issues (common in Gazebo classic)
if [[ -d /dev/dri ]]; then
  DOCKER_ARGS+=(--device=/dev/dri:/dev/dri)
  # Add host group ids if available (helps when container runs as non-root)
  if getent group video >/dev/null 2>&1; then
    DOCKER_ARGS+=(--group-add "$(getent group video | cut -d: -f3)")
  fi
  if getent group render >/dev/null 2>&1; then
    DOCKER_ARGS+=(--group-add "$(getent group render | cut -d: -f3)")
  fi
fi
 
if [[ "${USE_NVIDIA}" == "true" ]]; then
  echo "Running with NVIDIA enabled"
  DOCKER_ARGS+=(
    --gpus all
    -e "NVIDIA_DRIVER_CAPABILITIES=all"
    -e "__GLX_VENDOR_LIBRARY_NAME=nvidia"
    -e "__NV_PRIME_RENDER_OFFLOAD=1"
    -e "__VK_LAYER_NV_optimus=NVIDIA_only"
  )
else
  echo "Running without NVIDIA"
fi
 
# Launch demo inside container
docker run "${DOCKER_ARGS[@]}" "${IMAGE_NAME}" \
    bash -lc 'source /opt/ros/foxy/setup.bash && source /tmp/workspace/install/setup.bash && ros2 launch car_demo demo.launch.py'
 
 
# Revoke X access when done (optional)
xhost -local:root >/dev/null 2>&1 || true
 
