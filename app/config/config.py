import configparser
from pathlib import Path
from typing import Literal

from pydantic import BaseModel


config_parser = configparser.ConfigParser()
config_path = Path(f"{__file__}/../../config.ini")
with config_path.open(encoding="utf-8") as config_file:
    config_parser.read_file(config_file)


class DatabaseSettings(BaseModel):
    url: str


class LoggingSettings(BaseModel):
    level: Literal["CRITICAL", "FATAL", "ERROR", "WARN", "WARNING", "INFO", "DEBUG", "NOTSET"]


database_settings = DatabaseSettings.model_validate(config_parser["database"])
logging_settings = LoggingSettings.model_validate(config_parser["logging"])
