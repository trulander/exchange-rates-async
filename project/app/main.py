from fastapi import Depends, FastAPI

from app.models import CurrencyRates, CurrencyRatesCreate
# from .config import settings

from businesslogic import RequestCurrencyService
from interfaces import DataAccessInterface
from dataaccess import DataAccess

app = FastAPI()
service_request = lambda : RequestCurrencyService(data_access=DataAccess())

@app.get("/last_rate", response_model=CurrencyRates)
async def get_last_rate(data_access: DataAccessInterface = Depends(DataAccess)):
    result = await data_access.async_get_last_currency_rate()
    return result

@app.get("/list_rates", response_model=list[CurrencyRates])
async def get_list_rates(data_access: DataAccessInterface = Depends(DataAccess)):
    result = await data_access.async_get_list_currency_rates()
    return result

@app.get("/latest_rate", response_model=CurrencyRatesCreate)
async def get_latest_rate(service: RequestCurrencyService = Depends(service_request)):
    result = await service.request(1)
    return result

# @app.post("/create_rate", response_model=CurrencyRates)
# async def create_new_rate(currency_rate: CurrencyRatesCreate, data_access: DataAccessInterface = Depends(DataAccess)):
#     result = await data_access.async_create_currency_rate(currency_rate)
#     return result
