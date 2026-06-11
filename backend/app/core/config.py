"""Configuración central — variables de entorno tipadas."""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Tesis Assistant API"
    app_env: str = "development"
    app_port: int = 8000

    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/tesis_assistant"

    upload_dir: str = "./uploads"
    max_upload_mb: int = 25

    secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_expires_min: int = 60

    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
