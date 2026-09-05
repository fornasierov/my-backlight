#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_DIR="${MY_BACKLIGHT_CONFIG_DIR:-$HOME/.config/my-backlight}"
CONFIG_SOURCE="$ROOT_DIR/configs/config.yaml"
CONFIG_TARGET="$CONFIG_DIR/config.yaml"

if [[ ! -f "$CONFIG_SOURCE" ]]; then
    echo "Error: example configuration is missing: $CONFIG_SOURCE" >&2
    exit 1
fi

if [[ -e "$CONFIG_TARGET" ]]; then
    echo "Configuration already exists: $CONFIG_TARGET"
    echo "Existing configuration was preserved."
    exit 0
fi

mkdir -p "$CONFIG_DIR"
install -m 0644 "$CONFIG_SOURCE" "$CONFIG_TARGET"
echo "Created configuration: $CONFIG_TARGET"