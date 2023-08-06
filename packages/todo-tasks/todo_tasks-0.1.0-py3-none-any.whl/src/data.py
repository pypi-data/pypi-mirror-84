import json
import os
from pathlib import Path

from .models import Data, GlobalConfig


class DataLoader:
    def __init__(self, path: str = None) -> None:
        self._filename = path or Path(os.getcwd()) / ".tasks.json"
        self._global_config_filename = Path(os.path.expanduser("~")) / ".tasks.config.json"


    def exists(self) -> bool:
        return os.path.exists(self._filename)

    def init(self) -> None:
        with open(self._filename, "w+") as f:
            f.write(Data().json())

    def load(self) -> Data:
        with open(self._filename, "r") as f:
            return Data(**json.load(f))

    def create_global_config_if_not_exists(self) -> None:
        if not os.path.exists(self._global_config_filename):
            with open(self._global_config_filename, "w+") as f:
                f.write(GlobalConfig().json())

    def load_global_config(self) -> GlobalConfig:
        with open(self._global_config_filename, "r") as f:
            return GlobalConfig(**json.load(f))

    def save_global_config(self, global_config: GlobalConfig) -> None:
        with open(self._global_config_filename, "w+") as f:
            f.write(global_config.json())

    def drop(self) -> None:
        os.remove(self._filename)

    def save(self, data: Data) -> None:
        with open(self._filename, "w+") as f:
            f.write(data.json())
