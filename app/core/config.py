from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # API
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # Storage
    FRAMES_DIR: str

    # OCR
    OCR_MODEL: str
    OCR_IMAGE_WIDTH: int

    # YOLO
    YOLO_MODEL_PATH: str
    YOLO_CONFIDENCE: float

    class Config:
        env_file = ".env"

settings = Settings()