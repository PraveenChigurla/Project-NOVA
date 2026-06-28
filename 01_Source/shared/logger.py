"""
Project NOVA Logging Subsystem Initialization.
Defines standard logging interfaces and formats for observability across all NOVA modules.
"""

import logging
import os
import sys
from typing import Dict, Any


def setup_logger(name: str, config: Dict[str, Any]) -> logging.Logger:
    """
    Sets up a standard module-level logger according to the global configuration.
    
    Args:
        name: Name of the module.
        config: Dictionary containing logging parameters.
        
    Returns:
        logging.Logger: Preconfigured logger instance.
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers if logger is already configured
    if logger.handlers:
        return logger

    # Resolve log level
    level_str = config.get("level", "INFO").upper()
    level = getattr(logging, level_str, logging.INFO)
    logger.setLevel(level)

    # Standard format
    log_format = config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    formatter = logging.Formatter(log_format)

    # Console output handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File output handler (optional)
    if config.get("write_to_file", False):
        log_file_path = config.get("log_file_path", "logs/nova.log")
        # Ensure log directory exists
        log_dir = os.path.dirname(log_file_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
            
        file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
