"""
Configuration settings for the application
"""

from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # Directories
    DATA_DIR: Path = Path("/data")
    COLMAP_PROJECT_DIR: Path = Path("/app/colmap_project")
    SCRIPTS_DIR: Path = Path("/app/scripts")

    # Video settings
    VIDEO_FILENAME: str = "output3.mp4"
    MAX_FPS: int = 120
    MIN_FPS: int = 1

    # Processing settings
    PIPELINE_TIMEOUT: int = 3600  # 1 hour in seconds
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024 * 1024  # 5GB

    # Pipeline script
    PIPELINE_SCRIPT: str = "pipeline_colmap.sh"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Ensure directories exist
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.COLMAP_PROJECT_DIR.mkdir(parents=True, exist_ok=True)
