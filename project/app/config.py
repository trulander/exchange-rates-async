from pydantic import BaseSettings, Field


class Settings(BaseSettings):

    database_url: str = 'postgresql+asyncpg://dev:dev@localhost:5432/dev'

    celery_broker: str = 'redis://localhost:6379/0'
    celery_backend: str = 'redis://localhost:6379/1'
    celery_default_task_time_interval: float = 15.0

    url_to_endpoint_for_worker: str = 'http://localhost:8000/api/ratecurrency/latest/'

    # service coinmarketcap.com
    url_api_foreign_service_rates: str = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    api_key_service_rates: dict = {'CMC_PRO_API_KEY': 'd61bca4c-e9d3-40b9-8d82-abf9b057ffbd'}

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()