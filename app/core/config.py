from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "postgresql://admin:masterkey@db/db_project")

settings = Settings()