import logging

from app.config.config import logging_settings


def configure_logging() -> None:
    logging.basicConfig(level=logging_settings.level)
