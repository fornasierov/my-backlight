import json
import os
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .utils import clamp, hex_to_rgb, percent_to_intensity, resolve_color

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = Path(
    os.environ.get(
        "MY_BACKLIGHT_CONFIG_DIR",
        Path.home() / ".config" / "my-backlight",
    )
)
YAML_CONFIG_FILE = CONFIG_DIR / "config.yaml"
STATE_FILE = CONFIG_DIR / "state.json"


class YamlConfigModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class DeviceConfig(YamlConfigModel):
    hid_id: str
    firmware_report_id: int = Field(ge=0, le=255)
    color_report_id: int = Field(ge=0, le=255)
    required_kernel_module: str


class HidConfig(YamlConfigModel):
    ioctl_base: int
    host_byte: int = Field(ge=0, le=255)
    firmware_byte: int = Field(ge=0, le=255)


class DefaultsConfig(YamlConfigModel):
    color: str
    percent: int = Field(ge=0, le=100)
    last_on_percent: int = Field(ge=0, le=100)

    @field_validator("color")
    @classmethod
    def validate_color(cls, value: str) -> str:
        return resolve_color(value)


class AppConfig(YamlConfigModel):
    device: DeviceConfig
    hid: HidConfig
    defaults: DefaultsConfig


class RuntimeState(YamlConfigModel):
    color: str
    percent: int = Field(ge=0, le=100)
    last_on_percent: int = Field(ge=0, le=100)

    @field_validator("color")
    @classmethod
    def validate_color(cls, value: str) -> str:
        return resolve_color(value)


def load_app_config() -> AppConfig:
    try:
        with YAML_CONFIG_FILE.open() as config_file:
            raw_config = yaml.safe_load(config_file) or {}
    except FileNotFoundError as error:
        raise RuntimeError(
            f"Configuration file not found: {YAML_CONFIG_FILE}"
        ) from error
    except yaml.YAMLError as error:
        raise RuntimeError(f"Invalid YAML configuration: {YAML_CONFIG_FILE}") from error

    return AppConfig.model_validate(raw_config)


def default_runtime_state(app_config: AppConfig) -> RuntimeState:
    return RuntimeState(
        color=app_config.defaults.color,
        percent=app_config.defaults.percent,
        last_on_percent=app_config.defaults.last_on_percent,
    )


def load_runtime_state(app_config: AppConfig) -> RuntimeState:
    if not STATE_FILE.exists():
        return default_runtime_state(app_config)

    try:
        raw_state = json.loads(STATE_FILE.read_text())
        return RuntimeState.model_validate(raw_state)
    except (json.JSONDecodeError, ValueError):
        return default_runtime_state(app_config)


def save_runtime_state(state: RuntimeState) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(state.model_dump_json(indent=2) + "\n")


def get_saved_static_state(state: RuntimeState):
    r, g, b = hex_to_rgb(state.color)

    percent = state.percent
    if percent <= 0:
        percent = state.last_on_percent
        if percent <= 0:
            percent = 100

    percent = clamp(percent, 0, 100)
    intensity = percent_to_intensity(percent)

    return r, g, b, percent, intensity
