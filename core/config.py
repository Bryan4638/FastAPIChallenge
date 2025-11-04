import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = "FastAPI Challenge"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "clave-por-defecto")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))

    DATABASE_USER: str = os.getenv("DATABASE_USER", "postgres")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "password")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT", "5432")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "challenge_db")

    SQLALCHEMY_DATABASE_URL: str = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

    BACKEND_CORS_ORIGINS: list[str] = ["localhost", "127.0.0.1", "0.0.0.0"]

settings = Settings()
