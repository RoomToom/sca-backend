from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    CAT_API_URL: str = Field(default="https://api.thecatapi.com/v1/breeds")
    CAT_API_KEY: str | None = None
    DATABASE_URL: str = Field(default="sqlite:///./sca.db")
    API_V1_STR: str = Field(default="/api/v1")

settings = Settings()
