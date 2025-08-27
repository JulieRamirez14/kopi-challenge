"""
Application configuration.

Handles all environment variables and system configuration.
"""

import os
from typing import List

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """
    Main application configuration.
    
    Uses Pydantic BaseSettings for automatic type validation
    and loading from environment variables.
    """
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT") 
    debug_mode: bool = Field(default=False, env="DEBUG_MODE")
    
    # Conversation Settings
    max_conversation_history: int = Field(default=5, env="MAX_CONVERSATION_HISTORY")
    response_timeout_seconds: int = Field(default=30, env="RESPONSE_TIMEOUT_SECONDS")
    
    # Debate Configuration
    default_personality: str = Field(default="conspiracy_theorist", env="DEFAULT_PERSONALITY")
    enable_logging: bool = Field(default=True, env="ENABLE_LOGGING")
    
    # Deployment
    environment: str = Field(default="development", env="ENVIRONMENT")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # CORS Settings
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        env="CORS_ORIGINS"
    )
    
    # Optional: External APIs (for future enhancements)
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    anthropic_api_key: str = Field(default="", env="ANTHROPIC_API_KEY")
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment.lower() == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment.lower() == "production"
    
    def get_uvicorn_config(self) -> dict:
        """
        Get configuration for Uvicorn.
        
        Returns:
            Dictionary with Uvicorn configuration
        """
        return {
            "host": self.api_host,
            "port": self.api_port,
            "reload": self.is_development,
            "log_level": self.log_level.lower(),
            "access_log": self.enable_logging,
        }


# Global configuration instance
settings = Settings()


def get_settings() -> Settings:
    """
    Convenience function to get configuration.
    
    Returns:
        Configuration instance
    """
    return settings
