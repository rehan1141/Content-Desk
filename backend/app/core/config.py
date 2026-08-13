import os
from typing import List, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Content Desk Backend"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"

    # Server Defaults
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = True

    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:1420",
        "http://localhost:3000",
        "http://127.0.0.1:1420",
        "tauri://localhost",
    ]

    # Database Configuration (PostgreSQL primary with fallback URI)
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "rehanmultani")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "content_desk")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://rehanmultani@localhost:5432/content_desk"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
