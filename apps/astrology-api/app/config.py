from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    cors_origins: str = "http://localhost:3000"
    ephemeris_path: str | None = None
    default_ayanamsa: str = "lahiri"
    default_house_system: str = "whole-sign"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
