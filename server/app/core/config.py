import os
import sys
from pydantic_settings import BaseSettings
from pydantic import ValidationError
from dotenv import load_dotenv

# Load the .env file for local development
load_dotenv()

class Settings(BaseSettings):
    # Add Supabase credentials
    SUPABASE_URL: str
    SUPABASE_KEY: str

    # Remove the old DATABASE_URL
    # DATABASE_URL: str 
    
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    GEMINI_API_KEY: str

    class Config:
        env_file = ".env"

try:
    settings = Settings()
except ValidationError as e:
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", file=sys.stderr)
    print("!!!               CONFIGURATION ERROR                     !!!", file=sys.stderr)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", file=sys.stderr)
    print("The application failed to start because of missing environment variables.", file=sys.stderr)
    print("Please ensure you have set all the required variables in your deployment environment (e.g., Railway dashboard).", file=sys.stderr)
    print("A local '.env' file is for development and is NOT used in production deployments.", file=sys.stderr)
    print("\nMissing variables:", file=sys.stderr)
    for error in e.errors():
        # error['loc'] is a tuple of field names
        print(f"- {error['loc'][0]}", file=sys.stderr)
    print("\nRefer to the DEPLOY_README.md for a full list of required variables.", file=sys.stderr)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", file=sys.stderr)
    sys.exit(1)
