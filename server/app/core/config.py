import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    GEMINI_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()