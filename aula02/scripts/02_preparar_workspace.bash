#!/usr/bin/env bash
# Cria links para os quatro pacotes completos; nunca substitui pastas existentes.
set -eo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/ambiente.bash"
mkdir -p "$AULA02_WS/src" "$AULA02_DATA"
packages=(cartographer_slam map_server localization_server spot_recorder_interfaces)
for package in "${packages[@]}"; do
    source_path="$AULA02_DIR/exemplos/$package"
    target="$AULA02_WS/src/$package"
    if [[ -e "$target" || -L "$target" ]]; then
        if [[ "$(readlink -f "$target")" != "$source_path" ]]; then
            echo "Nao vou sobrescrever: $target. Confira o workspace antes de continuar." >&2
            exit 1
        fi
    else
        ln -s "$source_path" "$target"
    fi
done
cd "$AULA02_WS"
colcon list
colcon build --symlink-install --packages-up-to "${packages[@]}" \
    --event-handlers console_direct+
printf '\nEm CADA terminal: source %q\n' "$AULA02_DIR/scripts/ambiente.bash"
