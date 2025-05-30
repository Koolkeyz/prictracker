"""This file contains the configurations for the logger."""

import logging
from backend.config import get_settings
from uvicorn.logging import DefaultFormatter


settings = get_settings()

# Configure logging
LOG_FILE = "pricetracker.log"
LOG_LEVEL = logging.DEBUG
FORMAT_CONSOLE = "%(levelprefix)s %(name)s::%(funcName)s | %(message)s"
FORMAT_FILE = (
    "%(asctime)s | %(levelname)s | %(name)s [ function - %(funcName)s ] | %(message)s"
)


def getLogger(logger_name: str = "pricetracker") -> logging.Logger:
    """Return a logger object with the specified name."""
    # Passlib logger config to ignore __about__ version warning
    logging.getLogger("passlib").setLevel(logging.ERROR)

    formatter_console = DefaultFormatter(FORMAT_CONSOLE, datefmt="%Y-%m-%d %H:%M:%S")

    formatter_file = logging.Formatter(FORMAT_FILE, datefmt="%Y-%m-%d %H:%M:%S")

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(LOG_FILE)

    file_handler.setLevel(logging.INFO)
    console_handler.setLevel(LOG_LEVEL)

    file_handler.setFormatter(formatter_file)
    console_handler.setFormatter(formatter_console)

    logger = logging.getLogger(logger_name)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(LOG_LEVEL)
    return logger
