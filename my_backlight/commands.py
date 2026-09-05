from .config import AppConfig, RuntimeState, get_saved_static_state, save_runtime_state
from .hid import set_color, set_firmware_mode
from .utils import clamp, debug, hex_to_rgb, percent_to_intensity, resolve_color


def cmd_status(config: AppConfig, state: RuntimeState, dev_path):
    print("Device:", dev_path)
    print("HID ID:", config.device.hid_id)
    print("Saved color:", "#" + state.color)
    print("Saved brightness:", state.percent, "%")


def cmd_set(config: AppConfig, state: RuntimeState, dev_path, color, percent=None):
    color = resolve_color(color)
    r, g, b = hex_to_rgb(color)
    percent = state.percent if percent is None else clamp(int(percent), 0, 100)
    intensity = percent_to_intensity(percent)
    debug(f"cmd_set color={color} percent={percent} intensity={intensity}")

    set_firmware_mode(config, dev_path, False)
    set_color(config, dev_path, r, g, b, intensity)

    state.color = color
    state.percent = percent
    if percent > 0:
        state.last_on_percent = percent
    save_runtime_state(state)


def cmd_brightness(config: AppConfig, state: RuntimeState, dev_path, percent):
    r, g, b = hex_to_rgb(state.color)
    percent = clamp(int(percent), 0, 100)
    intensity = percent_to_intensity(percent)
    debug(f"cmd_brightness percent={percent} intensity={intensity}")

    set_firmware_mode(config, dev_path, False)
    set_color(config, dev_path, r, g, b, intensity)

    state.percent = percent
    if percent > 0:
        state.last_on_percent = percent
    save_runtime_state(state)


def cmd_off(config: AppConfig, state: RuntimeState, dev_path):
    r, g, b = hex_to_rgb(state.color)
    debug("cmd_off")

    if state.percent > 0:
        state.last_on_percent = state.percent

    set_firmware_mode(config, dev_path, False)
    set_color(config, dev_path, r, g, b, 0)
    state.percent = 0
    save_runtime_state(state)


def cmd_restore(config: AppConfig, state: RuntimeState, dev_path):
    r, g, b, percent, intensity = get_saved_static_state(state)
    debug(f"cmd_restore percent={percent} intensity={intensity}")

    set_firmware_mode(config, dev_path, False)
    set_color(config, dev_path, r, g, b, intensity)
    state.percent = percent
    save_runtime_state(state)
