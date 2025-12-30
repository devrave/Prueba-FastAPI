from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Aplicación
    APP_NAME: str = "Gestor de Tareas"
    APP_ENV: str = "local"
    DEBUG: bool = True
    
    # Seguridad - JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    
    # Base de datos
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
