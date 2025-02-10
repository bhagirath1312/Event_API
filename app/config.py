from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "4f8c3b8e72a1dcb57f9ac27492d8b1d3bfa5e324f1c6789da2b3f7c6d5e4a1f2"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "postgresql://postgres:Bhatti1312@localhost:5432/event_api"

settings = Settings()