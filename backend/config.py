from pydantic_settings import BaseSettings
from typing import List
import os
from typing import Dict, List, Optional
class Settings(BaseSettings):
    """
    Application configuration settings using Pydantic for validation.
    Environment variables can override these defaults.
    """
    
    # Agent Configuration
    AGENT_LOOP_INTERVAL: float = 2.0  # seconds between posts
    
    # Detection Pipeline Settings
    MIN_TRUST_SCORE: float = 0.5
    MAX_TRUST_SCORE: float = 1.0
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Content Types
    SUPPORTED_CONTENT_TYPES: List[str] = ["text", "image", "video", "audio"]
    
    # Fake Feed Settings
    FAKE_POST_TEMPLATES: List[str] = [
        "Breaking: {topic} causes major disruption in {location}",
        "Scientists discover {discovery} that could change {field}",
        "Local {authority} confirms {event} in {location}",
        "New study shows {claim} affects {demographic}",
        "Exclusive: {celebrity} spotted doing {activity} in {location}"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()
