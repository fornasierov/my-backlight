#!/usr/bin/env bash

set -euo pipefail

DEVICE="${1:-/dev/hidraw1}"
GROUP_NAME="my-backlight"

printf 'Current user: '
echo "$USER"
id
printf '\nDevice permissions:\n'
ls -l "$DEVICE" 2>&1 || true
printf '\nDevice ACL:\n'
getfacl --absolute-names "$DEVICE" 2>&1 || true
printf '\nUdev properties:\n'
udevadm info --query=property --name="$DEVICE" 2>&1 || true
printf '\nKernel module:\n'
if [[ -d /sys/module/asus_nb_wmi ]]; then
    echo 'asus-nb-wmi: loaded'
else
    echo 'asus-nb-wmi: not loaded'
fi
printf '\nGroup membership:\n'
if id -nG | tr ' ' '\n' | grep -Fxq "$GROUP_NAME"; then
    echo "Group '$GROUP_NAME': active"
else
    echo "Group '$GROUP_NAME': not active in this shell"
    echo 'Start a new login session after installation.'
fi
