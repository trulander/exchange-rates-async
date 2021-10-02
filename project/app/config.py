from pydantic import BaseSettings, Field


class Settings(BaseSettings):

    database_url: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/foo'

    celery_broker: str = 'redis://localhost:6379/0'
    celery_backend: str = 'redis://localhost:6379/1'
    celery_default_task_time_interval: float = 5.0

    # service coinmarketcap.com
    url_api_foreign_service_rates = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    api_key_service_rates = {'CMC_PRO_API_KEY': 'd61bca4c-e9d3-40b9-8d82-abf9b057ffbd'}

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()