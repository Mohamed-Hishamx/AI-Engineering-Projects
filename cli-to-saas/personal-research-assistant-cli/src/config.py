"""
Application settings and logging configuration.
Settings are loaded from environment variables or a `.env` file
using `pydantic-settings`, ensuring type validation at startup.
"""

import logging
import logging.config
import os
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    groq_api_key: str = Field(..., alias="GROQ_API_KEY")
    model: str = Field(default="llama-3.3-70b-versatile", alias="MODEL")
    temperature: float = Field(default=0.3, alias="TEMPERATURE")
    max_tokens: int = Field(default=1024, alias="MAX_TOKENS")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    model_config = {
        "env_file": ".env",
        "populate_by_name": True,
    }


def configure_logging(log_level: str = "INFO") -> None:
    os.makedirs("logs", exist_ok=True)
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {"format": "%(levelname)s | %(name)s | %(message)s"},
            "file": {
                "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "console",
                "stream": "ext://sys.stderr",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "file",
                "filename": "logs/assistant.log",
                "maxBytes": 1_000_000,
                "backupCount": 3,
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console", "file"]},
    })


# pydantic-settings reads .env automatically — no manual loading needed
try:
    settings = Settings()
except Exception:
    # Only used during pytest — no .env needed for mocked tests
    settings = Settings(
        GROQ_API_KEY="sk-fake-key-for-tests",
        MODEL="llama-3.3-70b-versatile",
        TEMPERATURE=0.3,
        MAX_TOKENS=1024,
        LOG_LEVEL="WARNING",
    )

configure_logging(settings.log_level)