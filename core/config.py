from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Challenge"
    DEBUG: bool = True
    
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "svbdjhavsdjkhavsj"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    DATABASE_USER = os.getenv("DB_USER", "postgres")
    DATABASE_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DATABASE_HOST = os.getenv("DB_HOST", "localhost")
    DATABASE_PORT = os.getenv("DB_PORT", "5432")
    DATABASE_NAME = os.getenv("DB_NAME", "challenge")

    SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    
    BACKEND_CORS_ORIGINS: list[str] = ["localhost", "127.0.0.1", "0.0.0.0"]
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
