import logging
from logging.config import dictConfig


_LOG_FORMAT = "%(asctime)s %(levelname)-8s [%(name)s] %(message)s"
_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


def configure_logging(log_level: str) -> None:
    """Configure application logging using the supplied log level."""
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": _LOG_FORMAT,
                    "datefmt": _DATE_FORMAT,
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": log_level,
                    "formatter": "default",
                    "stream": "ext://sys.stderr",
                }
            },
            "loggers": {
                "app": {
                    "level": log_level,
                    "handlers": ["console"],
                    "propagate": False,
                },
            },
            "root": {
                "level": log_level,
                "handlers": ["console"],
            },
        }
    )
