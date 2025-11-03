"""
Structured logging configuration using Loguru.

This module sets up application-wide logging with appropriate formatting and levels.
"""

import sys
from pathlib import Path
from loguru import logger

from core.config import settings


def setup_logger():
    """
    Configure logger with appropriate settings.
    
    Sets up console and file logging with structured format.
    """
    # Remove default handler
    logger.remove()
    
    # Console handler with colors
    logger.add(
        sys.stdout,
        level=settings.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
    )
    
    # File handler for errors
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logger.add(
        log_dir / "app.log",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="100 MB",
        retention="30 days",
        compression="zip",
    )
    
    logger.add(
        log_dir / "error.log",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="50 MB",
        retention="60 days",
        compression="zip",
        backtrace=True,
        diagnose=True,
    )
    
    logger.info(f"Logger initialized with level: {settings.log_level}")


# Initialize logger on module import
setup_logger()

