from pydantic import BaseSettings, Field


class Settings(BaseSettings):

    database_url: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/foo'
    celery_broker: str = 'redis://localhost:6379/0'
    celery_backend: str = 'redis://localhost:6379/1'
    celery_default_task_time_interval: float = 5.0

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()