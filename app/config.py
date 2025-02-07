# from pydantic_settings import BaseSettings
# from pathlib import Path
#
# class Settings(BaseSettings):
#     SECRET_KEY: str
#     DATABASE_URL: str
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
#
#     class Config:
#         env_file = Path(__file__).resolve().parent.parent / ".env"  # ✅ Ensure correct path
#         env_file_encoding = 'utf-8'
#
# settings = Settings()
#

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "4f8c3b8e72a1dcb57f9ac27492d8b1d3bfa5e324f1c6789da2b3f7c6d5e4a1f2"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

# Fix typo: Change `Setting` to `Settings`
settings = Settings()