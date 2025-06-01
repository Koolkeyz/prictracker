from pydantic_settings import BaseSettings
from functools import lru_cache

from typing import Optional


# Load settings from environment variables
class Settings(BaseSettings):
    MONGO_URI: str # MongoDB connection string
    MONGO_DB: str # name of the database
    JWT_SECRET: str # secret key for JWT
    JWT_ALGORITHM: Optional[str] # algorithm for JWT
    APP_HOST: str # host for the application

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    """
    Get settings from environment variables.
    """
    return Settings()

