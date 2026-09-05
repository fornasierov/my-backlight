import os
import pwd
from pathlib import Path

HIDIOCSFEATURE_BASE = 0xC0004806


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

SUPPORTED_DEVICES = {
    "0018:00000B05:000019B6": {
        "hid_name": "ITE5570:00 0B05:19B6",
        "model": "ASUS Vivobook S14 series (ITE5570 0x19B6)",
        "confirmed_models": [
            "ASUS Vivobook S14 (S5406SA)",
        ],
        "firmware_report_id": 0x0B,
        "color_report_id": 0x05,
        "rainbow_supported": True,
        "required_modules": ["asus-nb-wmi"],
    },
    "0018:00000B05:00005570": {
        "hid_name": "ITE5570:00 0B05:5570",
        "model": "ASUS Vivobook S series (ITE5570 0x5570)",
        "confirmed_models": [
            "ASUS Vivobook S16 (M5606K)",
            "ASUS Vivobook S16 (M5606WA)",
            "ASUS Vivobook S14 (M5406WA)",
        ],
        "firmware_report_id": 0x46,
        "color_report_id": 0x45,
        "rainbow_supported": False,
    },
}

HOST_BYTE = 0x00
FIRMWARE_BYTE = 0x01

ASUS_WMI_BASE = Path("/sys/kernel/debug/asus-nb-wmi")
ASUS_WMI_METHOD_ID = ASUS_WMI_BASE / "method_id"
ASUS_WMI_DEV_ID = ASUS_WMI_BASE / "dev_id"
ASUS_WMI_CTRL_PARAM = ASUS_WMI_BASE / "ctrl_param"
ASUS_WMI_DEVS = ASUS_WMI_BASE / "devs"

VERSION = "0.3.5"
PROJECT_URL = "https://github.com/vrgb-dev/vrgb"
