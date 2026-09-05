from pathlib import Path

from .config import AppConfig
from .utils import debug, die


def ensure_required_module(config: AppConfig):
    module_name = config.device.required_kernel_module
    module_path = Path(f"/sys/module/{module_name.replace('-', '_')}")
    if module_path.exists():
        return

    die(
        f"Required kernel module missing: {module_name}\n\n"
        f"Load it with: sudo modprobe {module_name}"
    )


def find_device(config: AppConfig):
    base = Path("/sys/class/hidraw")

    if not base.exists():
        die("No hidraw devices found")

    for dev in sorted(base.iterdir()):
        uevent = dev / "device" / "uevent"
        if not uevent.exists():
            continue

        values = {}
        for line in uevent.read_text(errors="ignore").splitlines():
            key, separator, value = line.partition("=")
            if separator:
                values[key] = value.strip()

        if values.get("HID_ID") == config.device.hid_id:
            path = f"/dev/{dev.name}"
            debug(f"Selected device: {path}")
            ensure_required_module(config)
            return path

    die(f"Supported HID device not found: {config.device.hid_id}")
