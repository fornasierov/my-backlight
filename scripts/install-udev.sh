#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
RULE_SOURCE="$ROOT_DIR/udev/99-my-backlight.rules"
RULE_TARGET="/etc/udev/rules.d/99-my-backlight.rules"
GROUP_NAME="my-backlight"

if [[ ! -f "$RULE_SOURCE" ]]; then
    echo "Error: tracked udev rule not found: $RULE_SOURCE" >&2
    exit 1
fi

echo "Installing tracked my-backlight udev rule:"
cat "$RULE_SOURCE"

sudo groupadd --force "$GROUP_NAME"
sudo usermod --append --groups "$GROUP_NAME" "$USER"
sudo install -o root -g root -m 0644 "$RULE_SOURCE" "$RULE_TARGET"

sudo udevadm control --reload-rules
sudo udevadm trigger --subsystem-match=hidraw

echo
echo "Installed: $RULE_TARGET"
echo "User '$USER' was added to group '$GROUP_NAME'."
echo "Start a new login session before using my-backlight."
