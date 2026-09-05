#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
RULE_SOURCE="$ROOT_DIR/udev/99-my-backlight.rules"
RULE_TARGET="/etc/udev/rules.d/99-my-backlight.rules"
EXPECTED_HID_PARENT="0018:0B05:19B6.*"

if [[ ! -f "$RULE_SOURCE" ]]; then
    echo "Error: source rule is missing: $RULE_SOURCE" >&2
    exit 1
fi

if [[ ! -f "$RULE_TARGET" ]]; then
    echo "Not installed: $RULE_TARGET"
    exit 1
fi

if ! cmp --silent "$RULE_SOURCE" "$RULE_TARGET"; then
    echo "Error: installed rule differs from tracked source." >&2
    diff -u "$RULE_SOURCE" "$RULE_TARGET" || true
    exit 1
fi

grep -Fq "KERNELS==\"$EXPECTED_HID_PARENT\"" "$RULE_SOURCE"
grep -Fq 'MODE="0660"' "$RULE_SOURCE"
grep -Fq 'GROUP="my-backlight"' "$RULE_SOURCE"

echo "Udev rule audit passed."
echo "Source:    $RULE_SOURCE"
echo "Installed: $RULE_TARGET"
cat "$RULE_SOURCE"
