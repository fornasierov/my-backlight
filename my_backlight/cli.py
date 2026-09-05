import sys

from . import utils
from .commands import (
    cmd_brightness,
    cmd_off,
    cmd_restore,
    cmd_set,
    cmd_status,
)
from .config import load_config
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
            "  vrgb status\n"
            "  vrgb set RRGGBB [percent]\n"
            "  vrgb brightness 0-100\n"
            "  vrgb off\n"
            "  vrgb restore"
        )
        sys.exit(1)

    cfg = load_config()
    command = args[0]

    if command == "status":
        cmd_status(cfg, find_device())
    elif command == "set":
        if len(args) < 2:
            utils.die("Missing color")
        percent = args[2] if len(args) > 2 else None
        cmd_set(cfg, find_device(), args[1], percent)
    elif command == "brightness":
        if len(args) < 2:
            utils.die("Missing percent")
        cmd_brightness(cfg, find_device(), args[1])
    elif command == "off":
        cmd_off(cfg, find_device())
    elif command == "restore":
        cmd_restore(cfg, find_device())


if __name__ == "__main__":
    try:
        main()
    except PermissionError:
        utils.die(
            "Permission denied to HID device. Run with sudo or install a udev rule."
        )
