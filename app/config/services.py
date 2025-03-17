import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
# from firecrawl import FirecrawlApp
from pydantic_settings import BaseSettings

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Services(BaseSettings):
    LLM_MODEL: str = os.getenv("LLM_MODEL", "claude-3-5-haiku-20241022")
    LLM_PROVIDER_API_KEY: str = os.getenv("LLM_PROVIDER_API_KEY")

    LANGFUSE_PUBLIC_KEY: str = os.getenv("LANGFUSE_PUBLIC_KEY")
    LANGFUSE_SECRET_KEY: str = os.getenv("LANGFUSE_SECRET_KEY")


@lru_cache()
def get_services() -> Services:
    return Services()


# firecrawl_app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))
