import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from redis import Redis

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    DEBUG: bool = os.environ.get("DEBUG", True)

    LANGFUSE_HOST: str = os.environ.get("LANGFUSE_HOST")
    LANGFUSE_PUBLIC_KEY: str = os.environ.get("LANGFUSE_PUBLIC_KEY")
    LANGFUSE_SECRET_KEY: str = os.environ.get("LANGFUSE_SECRET_KEY")


@lru_cache()
def get_settings() -> Settings:
    return Settings()


redis_client = Redis(
    host=os.environ.get("REDIS_HOST"),
    port=os.environ.get("REDIS_PORT"),
    db=os.environ.get("REDIS_DB"),
    password=os.environ.get("REDIS_PASSWORD"),
    socket_timeout=5,
    socket_connect_timeout=3,
    retry_on_timeout=False,
)
