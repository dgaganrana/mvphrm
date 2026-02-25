"""
Logging configuration for MVPHRM backend using structured logging
"""
import logging
import sys
from typing import Any
from pythonjsonlogger import jsonlogger
from functools import lru_cache
import json
from datetime import datetime


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter with additional context"""

    def add_fields(self, log_record: dict, record: logging.LogRecord, message_dict: dict) -> None:
        super().add_fields(log_record, record, message_dict)
        log_record["timestamp"] = datetime.utcnow().isoformat()
        log_record["level"] = record.levelname
        log_record["logger"] = record.name
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)


@lru_cache
def get_logger(name: str) -> logging.Logger:
    """Get or create a logger with structured JSON output"""
    logger = logging.getLogger(name)

    # Skip if handlers already configured
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # Remove any existing handlers
    logger.handlers.clear()

    # JSON handler for stderr
    json_handler = logging.StreamHandler(sys.stderr)
    json_handler.setLevel(logging.DEBUG)
    json_formatter = CustomJsonFormatter("%(message)s")
    json_handler.setFormatter(json_formatter)
    logger.addHandler(json_handler)

    # Prevent propagation to root logger
    logger.propagate = False

    return logger


def setup_logging() -> None:
    """Setup logging for all modules"""
    # Get root logger
    root_logger = get_logger("uvicorn.access")
    root_logger.setLevel(logging.INFO)

    # Configure uvicorn loggers
    for logger_name in ["uvicorn", "uvicorn.access", "uvicorn.error"]:
        logger = get_logger(logger_name)
        logger.setLevel(logging.INFO)

    # Configure app logger
    get_logger("mvphrm")


# Module-level logger instances
app_logger = get_logger("mvphrm.app")
db_logger = get_logger("mvphrm.db")
api_logger = get_logger("mvphrm.api")
