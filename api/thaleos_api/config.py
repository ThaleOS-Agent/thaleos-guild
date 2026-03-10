from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    thaleos_env: str = "dev"
    thaleos_log_level: str = "INFO"
    thaleos_cors_origins: str = "http://localhost:5173"

    thaleos_registry_ttl_seconds: int = 60

    thaleos_api_key: str | None = None

    # utilix service address (podman-compose service name by default)
    utilix_base_url: str = "http://utilix:8787"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()