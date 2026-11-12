from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_HOST: str
    
    model_config = SettingsConfigDict(
            env_file=Path(__file__).resolve().parent.parent / ".env",
            env_ignore_empty=True,
            extra="ignore",
        )
    
    @property
    def POSTGRES_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
        
    
    
settings = DatabaseSettings()
