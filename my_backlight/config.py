import json
import sys

from .constants import CONFIG_DIR, CONFIG_FILE
from .utils import clamp, hex_to_rgb, percent_to_intensity


def default_config():
    return {
        "color": "aa00ff",
        "percent": 100,
        "last_on_percent": 100,
    }


def load_config():
    if not CONFIG_FILE.exists():
        return default_config()

    try:
        cfg = json.loads(CONFIG_FILE.read_text())
    except json.JSONDecodeError:
        backup = CONFIG_FILE.with_suffix(CONFIG_FILE.suffix + ".bad")
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            CONFIG_FILE.replace(backup)
            print(
                f"Warning: config file corrupted. Backed up to {backup} and using defaults.",
                file=sys.stderr,
            )
        except OSError:
            print(
                "Warning: config file corrupted. Could not back it up; using defaults.",
                file=sys.stderr,
            )
        return default_config()

    defaults = default_config()

    cfg.setdefault("color", defaults["color"])
    cfg.setdefault("percent", defaults["percent"])
    cfg.setdefault("last_on_percent", defaults["last_on_percent"])

    try:
        r, g, b = hex_to_rgb(cfg["color"])
        cfg["color"] = f"{r:02x}{g:02x}{b:02x}"
    except SystemExit:
        cfg["color"] = defaults["color"]

    try:
        cfg["percent"] = clamp(int(cfg["percent"]), 0, 100)
    except (TypeError, ValueError):
        cfg["percent"] = defaults["percent"]

    try:
        cfg["last_on_percent"] = clamp(int(cfg["last_on_percent"]), 0, 100)
    except (TypeError, ValueError):
        cfg["last_on_percent"] = defaults["last_on_percent"]

    return cfg


def save_config(cfg):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))


def get_saved_static_state(cfg):
    r, g, b = hex_to_rgb(cfg["color"])

    p = int(cfg.get("percent", 100))
    if p <= 0:
        p = int(cfg.get("last_on_percent", 100))
        if p <= 0:
            p = 100

    p = clamp(p, 0, 100)
    intensity = percent_to_intensity(p)

    return r, g, b, p, intensity
