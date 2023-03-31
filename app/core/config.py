import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME:str = "Recap API"
    PROJECT_VERSION:str = "1.0.0"

    REDIS_HOST:str = os.getenv("REDIS_HOST")
    REDIS_PORT:str = os.getenv("REDIS_PORT", 6379) # default port
    API_VERSION:str = os.getenv("API_VERSION", "/api/v1")

    COINGECKO_BASE_URL:str = os.getenv("COINGECKO_BASE_URL")
    FOX_NEWS_BASE_URL:str = os.getenv("FOX_NEWS_BASE_URL")
    GUARDIAN_NEWS_BASE_URL:str = os.getenv("GUARDIAN_NEWS_BASE_URL")
    ABC_NEWS_BASE_URL:str = os.getenv("ABC_NEWS_BASE_URL")

settings = Settings()