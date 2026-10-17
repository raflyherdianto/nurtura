from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Nurtura Co-Parenting API"
    app_version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"
    debug: bool = False
    environment: str = "development"

    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8000

    # CORS configuration
    allowed_origins: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Google Gemini AI Configuration
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    gemini_temperature: float = 0.2

    # Vertex AI Configuration (Uses $300 GCP Trial Credit)
    use_vertex_ai: bool = False
    gcp_project_id: str = ""
    gcp_location: str = "us-central1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
