from pathlib import Path

from .constants import CONFIG_FILE, SUPPORTED_DEVICES
from .utils import debug, die


def module_loaded(name: str) -> bool:
    return Path(f"/sys/module/{name.replace('-', '_')}").exists()


def ensure_required_modules(devinfo):
    missing = [
        module
        for module in devinfo.get("required_modules", [])
        if not module_loaded(module)
    ]

    if not missing:
        return

    mods = " ".join(missing)
    first = missing[0]

    die(
        "Required kernel module missing: "
        + ", ".join(missing)
        + "\n\nThis device may ignore HID LampArray commands until the module is loaded."
        + "\n\nLoad once:\n"
        + f"  sudo modprobe {mods}"
        + "\n\nLoad at boot:\n"
        + f"  echo {first} | sudo tee /etc/modules-load.d/{first}.conf"
    )


def find_device():
    base = Path("/sys/class/hidraw")

    debug(f"Config file: {CONFIG_FILE}")

    if not base.exists():
        die("No hidraw devices found")

    best_match = None
    best_score = -1
    best_reason = "no match"

    for dev in sorted(base.iterdir()):
        uevent = dev / "device" / "uevent"

        if not uevent.exists():
            debug(f"{dev.name}: missing uevent")
            continue

        txt = uevent.read_text(errors="ignore")

        hid_id = None
        hid_name = None

        for line in txt.splitlines():
            if line.startswith("HID_ID="):
                hid_id = line.split("=", 1)[1].strip()
            elif line.startswith("HID_NAME="):
                hid_name = line.split("=", 1)[1].strip()

        score = -1
        reason = "no match"
        profile = None

        if hid_id in SUPPORTED_DEVICES:
            profile = SUPPORTED_DEVICES[hid_id]
            score = 100
            reason = "exact HID_ID match"
        else:
            for supported_hid_id, supported in SUPPORTED_DEVICES.items():
                if hid_name == supported["hid_name"]:
                    profile = supported
                    score = 90
                    reason = f"exact HID_NAME match ({supported_hid_id})"
                    break

        debug(
            f"{dev.name}: hid_id={hid_id} hid_name={hid_name} "
            f"score={score} reason={reason}"
        )

        if score > best_score and profile is not None:
            best_score = score
            best_reason = reason
            best_match = {
                "path": f"/dev/{dev.name}",
                "hid_id": hid_id,
                "hid_name": hid_name,
                "model": profile["model"],
                "confirmed_models": profile.get("confirmed_models", []),
                "firmware_report_id": profile["firmware_report_id"],
                "color_report_id": profile["color_report_id"],
                "rainbow_supported": profile.get("rainbow_supported", False),
                "required_modules": profile.get("required_modules", []),
            }

    if best_match:
        debug(f"Selected device: {best_match['path']} ({best_reason})")
        debug(
            "Using report IDs: "
            f"firmware=0x{best_match['firmware_report_id']:02X} "
            f"color=0x{best_match['color_report_id']:02X}"
        )
        debug(f"Matched model: {best_match['model']}")
        if best_match.get("required_modules"):
            debug("Required modules: " + ", ".join(best_match["required_modules"]))
        ensure_required_modules(best_match)
        return best_match

    die("VRGB HID device not found")
