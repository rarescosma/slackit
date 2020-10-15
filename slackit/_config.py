""" Horrible configuration singleton.
"""
from pathlib import Path
from typing import Optional

import yaml


def configure(from_yaml_file: Path) -> None:
    """Setup from yaml file."""
    Config.set(yaml.safe_load(from_yaml_file.read_text()))


class Config:
    """Config holder."""

    _config: dict

    @staticmethod
    def set(config: dict) -> None:
        """Set it."""
        Config._config = config

    @staticmethod
    def get(key: Optional[str] = None) -> dict:
        """Get it."""
        if key is None:
            return Config._config
        return Config._config[key]
