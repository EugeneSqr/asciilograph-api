from functools import lru_cache

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    rabbitmq_host: str
    rabbitmq_user: str
    rabbitmq_password: str

@lru_cache
def get_settings() -> Settings:
    return Settings()
