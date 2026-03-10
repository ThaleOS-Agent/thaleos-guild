from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    utilix_id: str = "utilix-local-1"
    utilix_port: int = 8787
    utilix_heartbeat_seconds: int = 5

    # where to register
    thaleos_api_url: str = "http://api:8080"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()