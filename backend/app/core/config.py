# backend/app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str = "dev-secret-key"
    database_url: str = "sqlite:///./budgetax.db"

    class Config:
        env_file = ".env"   # Look for a .env file in project root
        env_file_encoding = "utf-8"

settings = Settings()
