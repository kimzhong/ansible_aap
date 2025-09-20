from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    Application settings.
    """
    API_V1_STR: str = "/api/v1"
    # Add other settings here

    class Config:
        env_file = ".env"

settings = Settings()