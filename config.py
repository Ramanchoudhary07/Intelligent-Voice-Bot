"""
Configuration management for Intelligent Voice Bot
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # AWS Configuration (for Amazon Polly)
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-east-1"
    
    # Google Gemini Configuration (for Response Generation)
    gemini_api_key: Optional[str] = None
    
    # Hugging Face Configuration
    hugging_face_token: Optional[str] = None
    
    # Database Configuration
    database_url: Optional[str] = None
    mongo_uri: Optional[str] = None
    database_type: str = "postgresql"  # postgresql or mongodb
    
    # Backend API Configuration
    backend_api_url: Optional[str] = None
    
    # Audio Configuration
    audio_sample_rate: int = 16000
    audio_channels: int = 1
    audio_format: str = "pcm"
    
    # Analytics Configuration
    analytics_enabled: bool = True
    
    # Application Paths
    base_dir: Path = Path(__file__).parent
    audio_dir: Path = base_dir / "audio_files"
    logs_dir: Path = base_dir / "logs"
    analytics_dir: Path = base_dir / "analytics_data"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Create necessary directories
settings = Settings()

# Create directories if they don't exist
settings.audio_dir.mkdir(exist_ok=True)
settings.logs_dir.mkdir(exist_ok=True)
settings.analytics_dir.mkdir(exist_ok=True)

