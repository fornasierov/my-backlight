from pathlib import Path

from .constants import REQUIRED_KERNEL_MODULE, SUPPORTED_HID_ID
from .utils import debug, die


def ensure_required_module():
    module_path = Path(f"/sys/module/{REQUIRED_KERNEL_MODULE.replace('-', '_')}")
    if module_path.exists():
        return

    die(
        f"Required kernel module missing: {REQUIRED_KERNEL_MODULE}\n\n"
        f"Load it with: sudo modprobe {REQUIRED_KERNEL_MODULE}"
    )


def find_device():
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

        if values.get("HID_ID") == SUPPORTED_HID_ID:
            path = f"/dev/{dev.name}"
            debug(f"Selected device: {path}")
            ensure_required_module()
            return path

    die(f"Supported HID device not found: {SUPPORTED_HID_ID}")
