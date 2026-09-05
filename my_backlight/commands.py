from .asus_wmi import asus_wmi_rainbow
from .config import get_saved_static_state, save_config
from .constants import PROJECT_URL, VERSION
from .hid import set_color, set_firmware_mode
from .utils import clamp, debug, die, hex_to_rgb, percent_to_intensity


def cmd_about():
    print(
        r"""
                 _
__   ___ __ __ _| |__
\ \ / / '__/ _` | '_ \
 \ V /| | | (_| | |_) |
  \_/ |_|  \__, |_.__/ 
           |___/

RGB control for ASUS HID LampArray keyboards

Version: """
        + VERSION
        + """
"""
        + PROJECT_URL
        + """

No kernel mods. No daemon. Just HID.
"""
    )


def cmd_status(cfg, devinfo):
    print("Device:", devinfo["path"])
    print("Model:", devinfo["model"])
    print("HID ID:", devinfo["hid_id"])

    confirmed_models = devinfo.get("confirmed_models", [])
    if confirmed_models:
        print("Confirmed on:", ", ".join(confirmed_models))

    print(
        "OEM rainbow:",
        "supported"
        if devinfo.get("rainbow_supported", False)
        else "not supported / unknown",
    )

    required_modules = devinfo.get("required_modules", [])
    if required_modules:
        print("Required modules:", ", ".join(required_modules))

    print("Saved color:", "#" + cfg["color"])
    print("Saved brightness:", cfg["percent"], "%")
    print("Last-on brightness:", cfg["last_on_percent"], "%")
    print("Saved mode:", "firmware/autonomous" if cfg["autonomous"] else "host/static")
    debug("status complete")


def cmd_set(cfg, devinfo, color, percent=None):
    r, g, b = hex_to_rgb(color)

    if percent is None:
        percent = cfg["percent"]

    percent = clamp(int(percent), 0, 100)
    intensity = percent_to_intensity(percent)
    debug(f"cmd_set color={color} percent={percent} intensity={intensity}")

    set_firmware_mode(devinfo, False)
    set_color(devinfo, r, g, b, intensity)

    cfg["color"] = color.replace("#", "").lower()
    cfg["percent"] = percent
    if percent > 0:
        cfg["last_on_percent"] = percent
    cfg["autonomous"] = False
    save_config(cfg)


def cmd_brightness(cfg, devinfo, percent):
    r, g, b = hex_to_rgb(cfg["color"])

    percent = clamp(int(percent), 0, 100)
    intensity = percent_to_intensity(percent)
    debug(f"cmd_brightness percent={percent} intensity={intensity}")

    set_firmware_mode(devinfo, False)
    set_color(devinfo, r, g, b, intensity)

    cfg["percent"] = percent
    if percent > 0:
        cfg["last_on_percent"] = percent
    cfg["autonomous"] = False
    save_config(cfg)


def cmd_auto(cfg, devinfo, state):
    firmware_on = state == "on"
    debug(f"cmd_auto state={state}")

    if firmware_on:
        set_firmware_mode(devinfo, True)
        cfg["autonomous"] = True
        save_config(cfg)
    else:
        r, g, b, p, intensity = get_saved_static_state(cfg)
        debug(f"cmd_auto off -> restore percent={p} intensity={intensity}")
        set_firmware_mode(devinfo, False)
        set_color(devinfo, r, g, b, intensity)
        cfg["percent"] = p
        cfg["autonomous"] = False
        save_config(cfg)


def cmd_rainbow(cfg, devinfo, state):
    enable = state == "on"
    debug(f"cmd_rainbow state={state}")

    if not devinfo.get("rainbow_supported", False):
        if enable:
            die(
                "OEM rainbow is not supported for this device mapping. "
                "Static HID color control should still work."
            )

        r, g, b, p, intensity = get_saved_static_state(cfg)
        debug(
            "cmd_rainbow off on unsupported device -> "
            f"restore percent={p} intensity={intensity}"
        )
        set_firmware_mode(devinfo, False)
        set_color(devinfo, r, g, b, intensity)
        cfg["percent"] = p
        cfg["autonomous"] = False
        save_config(cfg)
        print(
            "OEM rainbow is not supported for this device mapping; restored saved static state."
        )
        return

    if enable:
        set_firmware_mode(devinfo, True)
        asus_wmi_rainbow(True)
        cfg["autonomous"] = True
        save_config(cfg)
    else:
        asus_wmi_rainbow(False)
        r, g, b, p, intensity = get_saved_static_state(cfg)
        debug(f"cmd_rainbow off -> restore percent={p} intensity={intensity}")
        set_firmware_mode(devinfo, False)
        set_color(devinfo, r, g, b, intensity)
        cfg["percent"] = p
        cfg["autonomous"] = False
        save_config(cfg)


def cmd_off(cfg, devinfo):
    r, g, b = hex_to_rgb(cfg["color"])
    debug("cmd_off")

    p = int(cfg.get("percent", 100))
    if p > 0:
        cfg["last_on_percent"] = p

    set_firmware_mode(devinfo, False)
    set_color(devinfo, r, g, b, 0)

    cfg["percent"] = 0
    cfg["autonomous"] = False
    save_config(cfg)


def cmd_restore(cfg, devinfo):
    if cfg.get("autonomous", False):
        debug("cmd_restore autonomous=True -> keep firmware mode")
        set_firmware_mode(devinfo, True)
        return

    r, g, b, p, intensity = get_saved_static_state(cfg)
    debug(f"cmd_restore percent={p} intensity={intensity}")

    set_firmware_mode(devinfo, False)
    set_color(devinfo, r, g, b, intensity)

    cfg["percent"] = p
    cfg["autonomous"] = False
    save_config(cfg)
