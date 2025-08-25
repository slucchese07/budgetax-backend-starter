from pydantic import BaseModel
import os

class Settings(BaseModel):
    api_key: str = os.getenv("API_KEY", "dev-secret-key")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./budgetax.db")

settings = Settings()
