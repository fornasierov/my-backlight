import fcntl
import os

from .constants import FIRMWARE_BYTE, HIDIOCSFEATURE_BASE, HOST_BYTE
from .utils import clamp, debug


def HIDIOCSFEATURE(length: int) -> int:
    return HIDIOCSFEATURE_BASE | (length << 16)


def hid_set_feature(dev_path, report_id, payload_bytes):
    buf = bytes([report_id]) + payload_bytes
    debug(
        f"hid_set_feature dev={dev_path} report=0x{report_id:02X} "
        f"payload={payload_bytes.hex()}"
    )
    fd = os.open(dev_path, os.O_RDWR | os.O_CLOEXEC)
    try:
        fcntl.ioctl(fd, HIDIOCSFEATURE(len(buf)), buf)
    finally:
        os.close(fd)


def set_firmware_mode(devinfo, enabled: bool):
    debug(f"set_firmware_mode enabled={enabled}")
    hid_set_feature(
        devinfo["path"],
        devinfo["firmware_report_id"],
        bytes([FIRMWARE_BYTE if enabled else HOST_BYTE]),
    )


def set_color(devinfo, r, g, b, intensity):
    debug(f"set_color r={r} g={g} b={b} intensity={intensity}")

    payload = bytes(
        [
            0x01,
            0x00,
            0x00,
            0x00,
            0x00,
            clamp(r, 0, 255),
            clamp(g, 0, 255),
            clamp(b, 0, 255),
            clamp(intensity, 0, 255),
        ]
    )

    hid_set_feature(devinfo["path"], devinfo["color_report_id"], payload)
