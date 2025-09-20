from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings.
    """
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "a_very_secret_key"
    ALGORITHM: str = "HS256"
    MONGODB_URL: str = "mongodb://localhost:27017"

    class Config:
        env_file = ".env"

settings = Settings()