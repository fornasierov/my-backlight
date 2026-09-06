#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
MANIFEST="$ROOT_DIR/packaging/installed-files.txt"
RULE_TARGET="/etc/udev/rules.d/99-my-backlight.rules"
GROUP_NAME="my-backlight"
DRY_RUN="${DRY_RUN:-0}"

if [[ ! -f "$MANIFEST" ]]; then
    echo "Error: ownership manifest not found: $MANIFEST" >&2
    exit 1
fi

if [[ "$DRY_RUN" != "1" ]]; then
    echo "This removes installed mkb files, configuration, the udev rule, and group."
    echo "It does not remove the source repository."
    read -r -p 'Type REMOVE to continue: ' confirmation
    [[ "$confirmation" == "REMOVE" ]] || { echo "Cancelled."; exit 0; }
fi

remove_path() {
    local path="$1"
    local expanded_path="$path"

    if [[ "$path" == '~/'* ]]; then
        expanded_path="$HOME/${path:2}"
    fi

    if [[ "$DRY_RUN" == "1" ]]; then
        echo "Would remove: $expanded_path"
    elif [[ -e "$expanded_path" || -L "$expanded_path" ]]; then
        if [[ "$expanded_path" == /etc/* || "$expanded_path" == /usr/* ]]; then
            sudo rm -rf -- "$expanded_path"
        else
            rm -rf -- "$expanded_path"
        fi
        echo "Removed: $expanded_path"
    else
        echo "Not present: $expanded_path"
    fi
}

while IFS= read -r path; do
    [[ -z "$path" ]] && continue
    [[ "$path" == \#* ]] && continue
    remove_path "$path"
done < "$MANIFEST"

if [[ "$DRY_RUN" == "1" ]]; then
    echo "Would reload udev and remove group: $GROUP_NAME"
    exit 0
fi

sudo udevadm control --reload-rules
sudo udevadm trigger --subsystem-match=hidraw

if getent group "$GROUP_NAME" >/dev/null; then
    sudo groupdel "$GROUP_NAME"
    echo "Removed group: $GROUP_NAME"
else
    echo "Group not present: $GROUP_NAME"
fi

if [[ -e "$RULE_TARGET" ]]; then
    echo "Warning: udev rule still exists: $RULE_TARGET" >&2
    exit 1
fi

echo "mkb purge complete."
