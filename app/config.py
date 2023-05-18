from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    project_name: str = "Vehicule API"
    api_prefix: str = "/v1"
    debug: bool = False
    database_url: str = "sqlite+aiosqlite:///./vins.db"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
