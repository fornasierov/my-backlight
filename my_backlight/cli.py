import sys

from . import utils
from .commands import (
    cmd_brightness,
    cmd_off,
    cmd_restore,
    cmd_set,
    cmd_status,
)
from .config import load_app_config, load_runtime_state
from .devices import find_device


def main():
    args = sys.argv[1:]

    if args and args[0] == "--debug":
        utils.DEBUG = True
        args = args[1:]

    if not args or args[0] not in {
        "status",
        "set",
        "brightness",
        "off",
        "restore",
    }:
        print(
            "Usage:\n"
            "  my-backlight status\n"
            "  my-backlight set RRGGBB [percent]\n"
            "  my-backlight brightness 0-100\n"
            "  my-backlight off\n"
            "  my-backlight restore"
        )
        sys.exit(1)

    config = load_app_config()
    state = load_runtime_state(config)
    command = args[0]

    if command == "status":
        cmd_status(config, state, find_device(config))
    elif command == "set":
        if len(args) < 2:
            utils.die("Missing color")
        percent = args[2] if len(args) > 2 else None
        cmd_set(config, state, find_device(config), args[1], percent)
    elif command == "brightness":
        if len(args) < 2:
            utils.die("Missing percent")
        cmd_brightness(config, state, find_device(config), args[1])
    elif command == "off":
        cmd_off(config, state, find_device(config))
    elif command == "restore":
        cmd_restore(config, state, find_device(config))


if __name__ == "__main__":
    try:
        main()
    except PermissionError:
        utils.die(
            "Permission denied to the HID device. Run `make install-udev`, "
            "then start a new login session and use `make check-access`."
        )
