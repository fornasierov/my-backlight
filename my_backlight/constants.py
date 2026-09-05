import os
import pwd
from pathlib import Path

HIDIOCSFEATURE_BASE = 0xC0004806
SUPPORTED_HID_ID = "0018:00000B05:000019B6"
FIRMWARE_REPORT_ID = 0x0B
COLOR_REPORT_ID = 0x05
HOST_BYTE = 0x00
FIRMWARE_BYTE = 0x01
REQUIRED_KERNEL_MODULE = "asus-nb-wmi"


def get_real_home() -> Path:
    sudo_user = os.environ.get("SUDO_USER")
    if sudo_user:
        try:
            return Path(pwd.getpwnam(sudo_user).pw_dir)
        except KeyError:
            pass
    return Path.home()


CONFIG_DIR = get_real_home() / ".config" / "vrgb"
CONFIG_FILE = CONFIG_DIR / "config.json"
