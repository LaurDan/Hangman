import functools

from pydantic import BaseSettings, Field

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"


class AppSettings(BaseSettings):
    host = Field("127.0.0.1")
    port = Field("8080")
    db_conn: str = Field(..., env="UPDATE_SRV_DB_CONNECTION_STRING")

    class Config:
        env_prefix = "update_service_"
        env_file = ".env"


@functools.lru_cache
def get_settings() -> dict:
    return AppSettings().dict()


setting = get_settings()
