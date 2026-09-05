#!/usr/bin/env bash

set -u

CONFIG_DIR="${MY_BACKLIGHT_CONFIG_DIR:-$HOME/.config/my-backlight}"
CONFIG_FILE="$CONFIG_DIR/config.yaml"
RULE_SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/udev/99-my-backlight.rules"
RULE_TARGET="/etc/udev/rules.d/99-my-backlight.rules"
GROUP_NAME="my-backlight"
DEVICE="${MY_BACKLIGHT_DEVICE:-/dev/hidraw1}"
FAILED=0

check() {
    local label="$1"
    local result="$2"
    if [[ "$result" == 0 ]]; then
        printf 'PASS  %s\n' "$label"
    else
        printf 'FAIL  %s\n' "$label"
        FAILED=1
    fi
}

echo "my-backlight doctor"
command -v poetry >/dev/null 2>&1
check "Poetry is installed" "$?"

[[ -f "$CONFIG_FILE" ]]
check "Configuration exists ($CONFIG_FILE)" "$?"

[[ -f "$RULE_TARGET" ]]
check "udev rule is installed" "$?"

if [[ -f "$RULE_TARGET" ]]; then
    cmp -s "$RULE_SOURCE" "$RULE_TARGET"
    check "Installed udev rule matches the repository" "$?"
fi

id -nG | tr ' ' '\n' | grep -Fxq "$GROUP_NAME"
check "Current session belongs to '$GROUP_NAME'" "$?"

if [[ -e "$DEVICE" ]]; then
    DEVICE_GROUP="$(stat -c '%G' "$DEVICE")"
    DEVICE_MODE="$(stat -c '%a' "$DEVICE")"
    [[ "$DEVICE_GROUP" == "$GROUP_NAME" && "$DEVICE_MODE" == "660" ]]
    check "Device access is configured ($DEVICE: group=$DEVICE_GROUP mode=$DEVICE_MODE)" "$?"
else
    echo "INFO  Device not present: $DEVICE"
fi

if [[ "$FAILED" != 0 ]]; then
    echo
    echo "Suggested fixes:"
    [[ -f "$CONFIG_FILE" ]] || echo "  make config-init"
    [[ -f "$RULE_TARGET" ]] || echo "  make install-system"
    if ! id -nG | tr ' ' '\n' | grep -Fxq "$GROUP_NAME"; then
        echo "  make activate-group  # use the new group in a shell now"
        echo "  Or log out and back in for a persistent group change."
    fi
    if [[ -e "$DEVICE" ]] && [[ "$DEVICE_GROUP" != "$GROUP_NAME" || "$DEVICE_MODE" != "660" ]]; then
        echo "  make install-system  # reload and apply the udev rule"
    fi
    exit 1
fi

echo "All checked setup items passed."