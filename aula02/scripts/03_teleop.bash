#!/usr/bin/env bash
# Inicie somente com a simulacao de mapeamento/localizacao, sem Nav2 comandando.
set -eo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/ambiente.bash"
topic_type="$(timeout 10 ros2 topic type /cmd_vel 2>/dev/null || true)"
case "$topic_type" in
    geometry_msgs/msg/TwistStamped) stamped=true ;;
    geometry_msgs/msg/Twist) stamped=false ;;
    *) echo "Tipo de /cmd_vel ausente/ambiguo: $topic_type. Inicie e confira o Gazebo." >&2; exit 1 ;;
esac
printf 'Tipo detectado: %s; stamped:=%s\n' "$topic_type" "$stamped"
frame_args=()
if [[ "$stamped" == true ]]; then
    frame_args=(-p frame_id:=base_footprint)
fi
exec ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args \
    -p stamped:="$stamped" -p use_sim_time:=true "${frame_args[@]}" \
    -p speed:=0.15 -p turn:=0.5
