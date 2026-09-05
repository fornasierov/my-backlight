from .config import save_config
from .hid import set_color, set_firmware_mode
from .utils import clamp, debug, die, hex_to_rgb, percent_to_intensity


def normalize_profile_name(name):
    name = name.strip()
    if not name:
        die("Profile name cannot be empty")
    return name


def get_profiles(cfg):
    profiles = cfg.get("profiles")
    if not isinstance(profiles, dict):
        cfg["profiles"] = {}
        profiles = cfg["profiles"]
    return profiles


def apply_profile(cfg, devinfo, profile, save=True):
    color = profile["color"]
    percent = clamp(int(profile["percent"]), 0, 100)
    autonomous = bool(profile["autonomous"])

    debug(f"apply_profile color={color} percent={percent} autonomous={autonomous}")

    cfg["color"] = color
    cfg["percent"] = percent
    if percent > 0:
        cfg["last_on_percent"] = percent
    cfg["autonomous"] = autonomous

    if autonomous:
        set_firmware_mode(devinfo, True)
    else:
        r, g, b = hex_to_rgb(color)
        intensity = percent_to_intensity(percent)
        set_firmware_mode(devinfo, False)
        set_color(devinfo, r, g, b, intensity)

    if save:
        save_config(cfg)


def cmd_profile_save(cfg, name):
    name = normalize_profile_name(name)
    profiles = get_profiles(cfg)

    profiles[name] = {
        "color": cfg["color"],
        "percent": cfg["percent"],
        "autonomous": cfg["autonomous"],
    }

    save_config(cfg)
    print(f"Saved profile: {name}")


def cmd_profile_load(cfg, devinfo, name):
    name = normalize_profile_name(name)
    profiles = get_profiles(cfg)

    if name not in profiles:
        die(f"Profile not found: {name}")

    apply_profile(cfg, devinfo, profiles[name], save=True)
    print(f"Loaded profile: {name}")


def cmd_profile_list(cfg):
    profiles = get_profiles(cfg)

    if not profiles:
        print("No profiles saved.")
        return

    print("Profiles:")
    for name in sorted(profiles):
        print(f"  {name}")


def cmd_profile_delete(cfg, name):
    name = normalize_profile_name(name)
    profiles = get_profiles(cfg)

    if name not in profiles:
        die(f"Profile not found: {name}")

    del profiles[name]
    save_config(cfg)
    print(f"Deleted profile: {name}")
