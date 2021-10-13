from fastapi import Depends, FastAPI

from app.models import CurrencyRate, CurrencyRateCreate
from app.businesslogic import RequestCurrencyService
from app.dataaccess import DataAccess

app = FastAPI()
service_request = lambda: RequestCurrencyService(data_access=DataAccess())

@app.get("/last_rate", response_model=CurrencyRate)
async def get_last_rate(service: RequestCurrencyService = Depends(service_request)):
    result = await service.get_last_rate()
    return result

@app.get("/list_rates", response_model=list[CurrencyRate])
async def get_list_rates(service: RequestCurrencyService = Depends(service_request)):
    result = await service.get_list_rates()
    return result

@app.get("/latest_rate", response_model=CurrencyRateCreate)
async def get_latest_rate(service: RequestCurrencyService = Depends(service_request)):
    result = await service.get_latest_rate(1)
    return result

# @app.post("/create_rate", response_model=CurrencyRate)
# async def create_new_rate(currency_rate: CurrencyRateCreate, data_access: DataAccessInterface = Depends(DataAccess)):
#     result = await data_access.async_create_currency_rate(currency_rate)
#     return result
