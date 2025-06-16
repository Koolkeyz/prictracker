"""This file contains the configurations for the logger."""

import logging
import sys
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Optional

from uvicorn.logging import ColourizedFormatter

from .settings import get_settings

settings = get_settings()

# Create logs directory if it doesn't exist
LOGS_DIR = Path(__file__).parent.parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)


class PriceTrackerFormatter(ColourizedFormatter):
    """
    Custom formatter that extends uvicorn's ColourizedFormatter
    to include additional context for the PriceTracker app.
    """

    def __init__(self, fmt: Optional[str] = None, use_colors: Optional[bool] = None):
        # Use uvicorn's default format if none provided
        if fmt is None:
            fmt = "%(levelprefix)s [%(name)s] %(message)s"
        super().__init__(fmt, use_colors)

    def formatMessage(self, record: logging.LogRecord) -> str:
        # Add custom context to the record if needed
        if hasattr(record, "endpoint"):
            record.name = f"{record.name}:{record.endpoint}"
        return super().formatMessage(record)


class PriceTrackerFileFormatter(logging.Formatter):
    """
    File formatter for PriceTracker logs without colors.
    """

    def __init__(self, fmt: Optional[str] = None):
        if fmt is None:
            fmt = "%(asctime)s - %(levelname)s - [%(name)s] %(message)s"
        super().__init__(fmt, datefmt="%Y-%m-%d %H:%M:%S")


def get_log_file_path(logger_name: str) -> Path:
    """
    Get the log file path for a given logger name.

    Args:
        logger_name: Name of the logger

    Returns:
        Path object for the log file
    """
    # Create daily log files
    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_name = logger_name.replace(".", "_")
    return LOGS_DIR / f"{safe_name}_{date_str}.log"


@lru_cache
def get_logger(name: str = "pricetracker") -> logging.Logger:
    """
    Get a configured logger instance that extends uvicorn's logging.

    Args:
        name: Logger name, defaults to "pricetracker"

    Returns:
        Configured logger instance with uvicorn-style formatting
    """
    logger = logging.getLogger(name)

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    # Create console handler with colored formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = PriceTrackerFormatter(use_colors=True)
    console_handler.setFormatter(console_formatter)

    # Create file handler with non-colored formatter
    log_file_path = get_log_file_path(name)
    file_handler = logging.FileHandler(log_file_path, mode="a", encoding="utf-8")
    file_formatter = PriceTrackerFileFormatter()
    file_handler.setFormatter(file_formatter)

    # Add both handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    return logger


def get_endpoint_logger(endpoint_name: str) -> logging.Logger:
    """
    Get a logger instance for a specific endpoint.

    Args:
        endpoint_name: Name of the endpoint (e.g., "auth", "products", "users")

    Returns:
        Logger configured for the specific endpoint
    """
    logger_name = f"pricetracker.{endpoint_name}"
    logger = logging.getLogger(logger_name)

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    # Create console handler with colored formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = PriceTrackerFormatter(
        fmt="%(levelprefix)s [%(name)s] %(message)s", use_colors=True
    )
    console_handler.setFormatter(console_formatter)

    # Create file handler with non-colored formatter
    log_file_path = get_log_file_path(logger_name)
    file_handler = logging.FileHandler(log_file_path, mode="a", encoding="utf-8")
    file_formatter = PriceTrackerFileFormatter()
    file_handler.setFormatter(file_formatter)

    # Add both handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    return logger


def log_request(
    logger: logging.Logger,
    method: str,
    path: str,
    status_code: int,
    process_time: float,
    client_ip: str = None,
):
    """
    Log HTTP request information in uvicorn style.

    Args:
        logger: Logger instance
        method: HTTP method
        path: Request path
        status_code: HTTP status code
        process_time: Request processing time in seconds
        client_ip: Client IP address (optional)
    """
    client_info = f" - {client_ip}" if client_ip else ""
    logger.info(f'"{method} {path}" {status_code} - {process_time:.2f}s{client_info}')


def log_startup_event(logger: logging.Logger, event: str, details: str = None):
    """
    Log application startup events in uvicorn style.

    Args:
        logger: Logger instance
        event: Event description
        details: Additional details (optional)
    """
    message = event
    if details:
        message += f" - {details}"
    logger.info(message)


def log_error(logger: logging.Logger, error: Exception, context: str = None):
    """
    Log errors with proper formatting and context.

    Args:
        logger: Logger instance
        error: Exception instance
        context: Additional context information
    """
    error_msg = f"{type(error).__name__}: {str(error)}"
    if context:
        error_msg = f"{context} - {error_msg}"
    logger.error(error_msg, exc_info=True)


def log_database_operation(
    logger: logging.Logger,
    operation: str,
    collection: str,
    result: dict = None,
    duration: float = None,
):
    """
    Log database operations with timing information.

    Args:
        logger: Logger instance
        operation: Database operation (e.g., "find", "insert", "update")
        collection: MongoDB collection name
        result: Operation result (optional)
        duration: Operation duration in seconds (optional)
    """
    msg = f"DB {operation.upper()} on {collection}"
    if duration:
        msg += f" - {duration:.3f}s"
    if result and isinstance(result, dict):
        if "acknowledged" in result:
            msg += f" - {'success' if result['acknowledged'] else 'failed'}"
        if "matched_count" in result:
            msg += f" - matched: {result['matched_count']}"
        if "modified_count" in result:
            msg += f" - modified: {result['modified_count']}"

    logger.info(msg)


def get_log_files() -> list[Path]:
    """
    Get all log files in the logs directory.

    Returns:
        List of Path objects for log files
    """
    return list(LOGS_DIR.glob("*.log"))


def clean_old_logs(days_to_keep: int = 30):
    """
    Remove log files older than specified days.

    Args:
        days_to_keep: Number of days to keep logs (default: 30)
    """
    from datetime import timedelta

    cutoff_date = datetime.now() - timedelta(days=days_to_keep)

    for log_file in get_log_files():
        try:
            # Get file creation time
            file_time = datetime.fromtimestamp(log_file.stat().st_mtime)
            if file_time < cutoff_date:
                log_file.unlink()
                print(f"Removed old log file: {log_file.name}")
        except Exception as e:
            print(f"Error removing log file {log_file.name}: {e}")


def get_log_file_size(logger_name: str) -> int:
    """
    Get the size of the current log file for a logger.

    Args:
        logger_name: Name of the logger

    Returns:
        File size in bytes, 0 if file doesn't exist
    """
    log_file = get_log_file_path(logger_name)
    try:
        return log_file.stat().st_size
    except FileNotFoundError:
        return 0


def rotate_log_file(logger_name: str, max_size_mb: int = 10):
    """
    Rotate log file if it exceeds maximum size.

    Args:
        logger_name: Name of the logger
        max_size_mb: Maximum file size in MB before rotation
    """
    log_file = get_log_file_path(logger_name)
    max_size_bytes = max_size_mb * 1024 * 1024

    if log_file.exists() and log_file.stat().st_size > max_size_bytes:
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime("%H%M%S")
        backup_name = f"{log_file.stem}_{timestamp}_backup.log"
        backup_path = log_file.parent / backup_name

        # Move current log to backup
        log_file.rename(backup_path)
        print(f"Rotated log file: {log_file.name} -> {backup_name}")


# Pre-configured loggers for common use cases
main_logger = get_logger("pricetracker")
auth_logger = get_endpoint_logger("auth")
products_logger = get_endpoint_logger("products")
users_logger = get_endpoint_logger("users")
scrapers_logger = get_endpoint_logger("scrapers")
config_logger = get_endpoint_logger("config")
