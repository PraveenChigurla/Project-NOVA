import logging
from pydantic_settings import BaseSettings, SettingsConfigDict

class NovaConfig(BaseSettings):
    """
    Project NOVA Configuration.
    Loaded from environment variables or a .env file.
    """
    log_level: str = "INFO"
    environment: str = "development"
    event_bus_max_queue_size: int = 1000
    
    model_config = SettingsConfigDict(
        env_prefix="NOVA_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def get_log_level(self) -> int:
        """Parse log level string to logging module constant."""
        level = self.log_level.upper()
        return getattr(logging, level, logging.INFO)
