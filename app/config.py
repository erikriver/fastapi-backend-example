from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    project_name: str = "Vehicule API"
    api_prefix: str = "/v1"
    debug: bool = False
    database_url: str = "sqlite+aiosqlite:///./vins.db"

    secret_key: str = "so_secret!!!"
    access_token_expire_minutes: int = 10
    algorithm: str = "HS256"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
