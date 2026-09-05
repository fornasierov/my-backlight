import sys

from . import utils
from .commands import (
    cmd_about,
    cmd_auto,
    cmd_brightness,
    cmd_off,
    cmd_rainbow,
    cmd_restore,
    cmd_set,
    cmd_status,
)
from .config import load_config
from .constants import ASUS_WMI_BASE
from .devices import find_device
from .profiles import (
    cmd_profile_delete,
    cmd_profile_list,
    cmd_profile_load,
    cmd_profile_save,
)


def main():
    args = sys.argv[1:]

    if args and args[0] == "--debug":
        utils.DEBUG = True
        args = args[1:]

    if len(args) < 1:
        print(
            """Usage:
  vrgb status
  vrgb set RRGGBB [percent]
  vrgb brightness 0-100
  vrgb auto on|off
  vrgb rainbow on|off
  vrgb off
  vrgb restore
  vrgb profile save NAME
  vrgb profile load NAME
  vrgb profile list
  vrgb profile delete NAME
  vrgb about

----------------------------------------
Tip: use --debug before the command for diagnostic output
Example: vrgb --debug status
"""
        )
        sys.exit(1)

    cfg = load_config()
    cmd = args[0]

    known_commands = {
        "status",
        "set",
        "brightness",
        "auto",
        "rainbow",
        "off",
        "restore",
        "profile",
        "about",
    }

    if cmd not in known_commands:
        utils.die("Unknown command")

    if cmd == "status":
        devinfo = find_device()
        cmd_status(cfg, devinfo)

    elif cmd == "set":
        if len(args) < 2:
            utils.die("Missing color")
        devinfo = find_device()
        percent = args[2] if len(args) > 2 else None
        cmd_set(cfg, devinfo, args[1], percent)

    elif cmd == "brightness":
        if len(args) < 2:
            utils.die("Missing percent")
        devinfo = find_device()
        cmd_brightness(cfg, devinfo, args[1])

    elif cmd == "auto":
        if len(args) < 2 or args[1] not in ["on", "off"]:
            utils.die("auto requires 'on' or 'off'")
        devinfo = find_device()
        cmd_auto(cfg, devinfo, args[1])

    elif cmd == "rainbow":
        if len(args) < 2 or args[1] not in ["on", "off"]:
            utils.die("rainbow requires 'on' or 'off'")
        devinfo = find_device()
        cmd_rainbow(cfg, devinfo, args[1])

    elif cmd == "off":
        devinfo = find_device()
        cmd_off(cfg, devinfo)

    elif cmd == "restore":
        devinfo = find_device()
        cmd_restore(cfg, devinfo)

    elif cmd == "profile":
        if len(args) < 2:
            utils.die("profile requires a subcommand: save, load, list, or delete")

        subcmd = args[1]

        if subcmd == "save":
            if len(args) < 3:
                utils.die("profile save requires a name")
            cmd_profile_save(cfg, args[2])
        elif subcmd == "load":
            if len(args) < 3:
                utils.die("profile load requires a name")
            devinfo = find_device()
            cmd_profile_load(cfg, devinfo, args[2])
        elif subcmd == "list":
            cmd_profile_list(cfg)
        elif subcmd == "delete":
            if len(args) < 3:
                utils.die("profile delete requires a name")
            cmd_profile_delete(cfg, args[2])
        else:
            utils.die("profile requires a subcommand: save, load, list, or delete")

    elif cmd == "about":
        cmd_about()

    else:
        utils.die("Unknown command")


if __name__ == "__main__":
    try:
        main()
    except PermissionError as e:
        path = getattr(e, "filename", None)
        if path and str(path).startswith(str(ASUS_WMI_BASE)):
            utils.die(
                "Permission denied to ASUS WMI debugfs. OEM rainbow requires sudo/root."
            )
        utils.die(
            "Permission denied to HID device. Run with sudo or install a udev rule."
        )
