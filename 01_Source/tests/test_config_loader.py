"""
Unit tests for Project NOVA configuration loading and logging helper.
"""

import os
import sys
import json
import tempfile
import pytest
from typing import Generator

# Add the 01_Source directory to sys.path to allow direct imports of core/shared modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.config_loader import ConfigurationLoader
from shared.logger import setup_logger


@pytest.fixture
def temp_config_file() -> Generator[str, None, None]:
    """
    Creates a temporary default_settings.json file for testing configuration loader.
    """
    test_data = {
        "platform": {
            "version": "0.1.0-test",
            "environment": "testing"
        },
        "logging": {
            "level": "DEBUG",
            "write_to_file": False
        }
    }
    
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False, encoding="utf-8") as f:
        json.dump(test_data, f)
        temp_path = f.name
        
    yield temp_path
    
    if os.path.exists(temp_path):
        os.remove(temp_path)


def test_config_loader_reads_data(temp_config_file: str) -> None:
    """
    Verifies that the ConfigurationLoader successfully reads settings from files.
    """
    loader = ConfigurationLoader(temp_config_file)
    assert loader.get("platform.version") == "0.1.0-test"
    assert loader.get("platform.environment") == "testing"
    assert loader.get("logging.level") == "DEBUG"
    assert loader.get("nonexistent.key", "default_val") == "default_val"


def test_logger_setup() -> None:
    """
    Verifies that setup_logger returns a valid logger instance and respects configured level.
    """
    config = {
        "level": "ERROR",
        "write_to_file": False
    }
    logger = setup_logger("test_module", config)
    assert logger.name == "test_module"
    assert logger.level == 40  # logging.ERROR
