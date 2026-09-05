#!/usr/bin/env bash

set -euo pipefail

RULE_TARGET="/etc/udev/rules.d/99-my-backlight.rules"

if [[ -f "$RULE_TARGET" ]]; then
    sudo rm -- "$RULE_TARGET"
    echo "Removed: $RULE_TARGET"
else
    echo "Not installed: $RULE_TARGET"
fi

sudo udevadm control --reload-rules
sudo udevadm trigger --subsystem-match=hidraw
