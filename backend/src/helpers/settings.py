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
    ADMIN_USERNAME: str # username for the admin account
    ADMIN_PASSWORD: str # password for the admin account
    ADMIN_EMAIL: str # email for the admin account
    SMTP_HOST: str # SMTP server host
    SMTP_PORT: str # SMTP server port
    SMTP_USERNAME: str # SMTP server username
    SMTP_PASSWORD: str # SMTP server password
    SMTP_FROM_NAME: str # name to display in the "from" field of emails
    SMTP_FROM_EMAIL: str # email address to use in the "from" field of emails

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    """
    Get settings from environment variables.
    """
    return Settings()
