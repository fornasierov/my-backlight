from .config import get_saved_static_state, save_config
from .constants import SUPPORTED_HID_ID
from .hid import set_color, set_firmware_mode
from .utils import clamp, debug, hex_to_rgb, percent_to_intensity


def cmd_status(cfg, dev_path):
    print("Device:", dev_path)
    print("HID ID:", SUPPORTED_HID_ID)
    print("Saved color:", "#" + cfg["color"])
    print("Saved brightness:", cfg["percent"], "%")


def cmd_set(cfg, dev_path, color, percent=None):
    r, g, b = hex_to_rgb(color)
    percent = cfg["percent"] if percent is None else clamp(int(percent), 0, 100)
    intensity = percent_to_intensity(percent)
    debug(f"cmd_set color={color} percent={percent} intensity={intensity}")

    set_firmware_mode(dev_path, False)
    set_color(dev_path, r, g, b, intensity)

    cfg["color"] = color.replace("#", "").lower()
    cfg["percent"] = percent
    if percent > 0:
        cfg["last_on_percent"] = percent
    save_config(cfg)


def cmd_brightness(cfg, dev_path, percent):
    r, g, b = hex_to_rgb(cfg["color"])
    percent = clamp(int(percent), 0, 100)
    intensity = percent_to_intensity(percent)
    debug(f"cmd_brightness percent={percent} intensity={intensity}")

    set_firmware_mode(dev_path, False)
    set_color(dev_path, r, g, b, intensity)

    cfg["percent"] = percent
    if percent > 0:
        cfg["last_on_percent"] = percent
    save_config(cfg)


def cmd_off(cfg, dev_path):
    r, g, b = hex_to_rgb(cfg["color"])
    debug("cmd_off")

    if cfg["percent"] > 0:
        cfg["last_on_percent"] = cfg["percent"]

    set_firmware_mode(dev_path, False)
    set_color(dev_path, r, g, b, 0)
    cfg["percent"] = 0
    save_config(cfg)


def cmd_restore(cfg, dev_path):
    r, g, b, percent, intensity = get_saved_static_state(cfg)
    debug(f"cmd_restore percent={percent} intensity={intensity}")

    set_firmware_mode(dev_path, False)
    set_color(dev_path, r, g, b, intensity)
    cfg["percent"] = percent
    save_config(cfg)
