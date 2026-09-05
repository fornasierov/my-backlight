from .constants import (
    ASUS_WMI_BASE,
    ASUS_WMI_CTRL_PARAM,
    ASUS_WMI_DEV_ID,
    ASUS_WMI_DEVS,
    ASUS_WMI_METHOD_ID,
)
from .utils import debug, die


def asus_wmi_write(method_id: str, dev_id: str, ctrl_param: str):
    ASUS_WMI_METHOD_ID.write_text(method_id)
    ASUS_WMI_DEV_ID.write_text(dev_id)
    ASUS_WMI_CTRL_PARAM.write_text(ctrl_param)

    try:
        _ = ASUS_WMI_DEVS.read_text(errors="ignore")
    except OSError as e:
        debug(f"ASUS WMI devs read failed: {e}")
        die("OEM rainbow not available: ASUS WMI exposed no usable device.")


def asus_wmi_rainbow(enable: bool):
    debug(f"asus_wmi_rainbow enable={enable}")

    if not ASUS_WMI_BASE.exists():
        die("OEM rainbow not supported on this system.")

    for p in (
        ASUS_WMI_METHOD_ID,
        ASUS_WMI_DEV_ID,
        ASUS_WMI_CTRL_PARAM,
        ASUS_WMI_DEVS,
    ):
        if not p.exists():
            die("OEM rainbow interface incomplete.")

    asus_wmi_write(
        "0x00000001",
        "0x0005002f",
        "0x00000000" if enable else "0x00000001",
    )
