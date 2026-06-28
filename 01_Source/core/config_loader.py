"""
Project NOVA Configuration Loader.
Manages loading, parsing, and resolving configuration variables for the NOVA platform.
"""

import json
import os
from typing import Dict, Any, Optional


class ConfigurationLoader:
    """
    ConfigurationLoader is responsible for initializing the platform configuration
    by merging default settings, file-based configurations, and environment overrides.
    """

    def __init__(self, default_config_path: str) -> None:
        self.default_config_path = default_config_path
        self._config: Dict[str, Any] = {}
        self.load_configuration()

    def load_configuration(self) -> None:
        """
        Loads settings from the default JSON configuration file, then checks for local 
        configuration overrides or environment variables.
        """
        if not os.path.exists(self.default_config_path):
            raise FileNotFoundError(
                f"Default configuration file not found at {self.default_config_path}"
            )

        with open(self.default_config_path, "r", encoding="utf-8") as f:
            self._config = json.load(f)

        # Merge local overrides if they exist (local settings are not committed to git)
        local_config_path = os.path.join(
            os.path.dirname(self.default_config_path), "local_settings.json"
        )
        if os.path.exists(local_config_path):
            with open(local_config_path, "r", encoding="utf-8") as f:
                local_config = json.load(f)
                self._deep_merge(self._config, local_config)

    def get(self, key_path: str, default: Optional[Any] = None) -> Any:
        """
        Retrieves a configuration value using dot notation.
        
        Example:
            loader.get("logging.level", "INFO")
        """
        keys = key_path.split(".")
        current: Any = self._config
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current

    def _deep_merge(self, base: Dict[str, Any], overrides: Dict[str, Any]) -> None:
        """
        Recursively merges two dictionaries.
        """
        for key, value in overrides.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
