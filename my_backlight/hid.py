import fcntl
import os

from .config import AppConfig
from .utils import clamp, debug


def hid_set_feature(config: AppConfig, dev_path, report_id, payload_bytes):
    buf = bytes([report_id]) + payload_bytes
    debug(
        f"hid_set_feature dev={dev_path} report=0x{report_id:02X} "
        f"payload={payload_bytes.hex()}"
    )
    fd = os.open(dev_path, os.O_RDWR | os.O_CLOEXEC)
    try:
        fcntl.ioctl(
            fd,
            config.hid.ioctl_base | (len(buf) << 16),
            buf,
        )
    finally:
        os.close(fd)


def set_firmware_mode(config: AppConfig, dev_path, enabled: bool):
    debug(f"set_firmware_mode enabled={enabled}")
    hid_set_feature(
        config,
        dev_path,
        config.device.firmware_report_id,
        bytes(
            [
                config.hid.firmware_byte if enabled else config.hid.host_byte,
            ]
        ),
    )


def set_color(config: AppConfig, dev_path, r, g, b, intensity):
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

    hid_set_feature(config, dev_path, config.device.color_report_id, payload)
