from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """
    Application configuration settings using Pydantic for validation.
    Environment variables can override these defaults.
    """

    # Debug Configuration
    DEBUG: bool = True                # enable or disable debug logs

    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # Detection Pipeline Settings
    MIN_TRUST_SCORE: float = 0.5
    MAX_TRUST_SCORE: float = 1.0

    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Content Types
    SUPPORTED_CONTENT_TYPES: List[str] = ["text", "image", "video", "audio"]

    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()

# Export commonly used settings for easier imports
DEBUG = settings.DEBUG
API_HOST = settings.API_HOST
API_PORT = settings.API_PORT
