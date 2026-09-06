#!/usr/bin/env bash

set -u

HELPER="${MKB_HID_HELPER:-/usr/local/libexec/mkb-hid}"
RULE_SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/udev/99-my-backlight.rules"
RULE_TARGET="/etc/udev/rules.d/99-my-backlight.rules"
GROUP_NAME="my-backlight"
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
command -v mkb >/dev/null 2>&1
check "mkb command is installed" "$?"

[[ -x "$HELPER" ]]
check "HID helper is installed ($HELPER)" "$?"

[[ -f "$RULE_TARGET" ]]
check "udev rule is installed" "$?"

if [[ -f "$RULE_TARGET" ]]; then
    cmp -s "$RULE_SOURCE" "$RULE_TARGET"
    check "Installed udev rule matches the repository" "$?"
fi

id -nG | tr ' ' '\n' | grep -Fxq "$GROUP_NAME"
check "Current session belongs to '$GROUP_NAME'" "$?"

if [[ "$FAILED" != 0 ]]; then
    echo
    echo "Suggested fixes:"
    [[ -x "$HELPER" ]] || echo "  make install"
    [[ -f "$RULE_TARGET" ]] || echo "  make install"
    if ! id -nG | tr ' ' '\n' | grep -Fxq "$GROUP_NAME"; then
        echo "  make activate-group  # use the new group in a shell now"
        echo "  Or log out and back in for a persistent group change."
    fi
    exit 1
fi

echo "All checked setup items passed."