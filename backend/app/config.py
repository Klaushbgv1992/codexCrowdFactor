from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

import yaml


@lru_cache
def load_yaml(path_env: str, default_path: str) -> dict[str, Any]:
    path = os.getenv(path_env, default_path)
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def settings() -> dict[str, Any]:
    return load_yaml("CONFIG_PATH", "config/settings.yaml")


def scenes() -> dict[str, Any]:
    return load_yaml("SCENES_PATH", "config/scenes.yaml")
