import datetime
from functools import lru_cache
from fastapi import Depends, FastAPI
from sqlalchemy.future import select
from sqlalchemy import insert, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import Currencies, CurrencyRates, CurrenciesBase, CurrencyRatesBase, CurrenciesCreate, CurrencyRatesCreate
from .config import settings

app = FastAPI()


@app.get("/last_rate")
async def get_last_rate(session: AsyncSession = Depends(get_session)):
    request = await session.execute(select(CurrencyRates).order_by(desc(CurrencyRates.id)))
    result = request.scalars().first()
    return result


@app.get("/list_rates", response_model=list[CurrencyRates])
async def get_list_rates(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(CurrencyRates))
    currency_rates: list[CurrencyRates] = result.scalars().all()
    return [CurrencyRates(
        id = rate.id,
        currency = rate.currency,
        date_added = rate.date_added,
        actual_date = rate.actual_date,
        price_usd = rate.price_usd,
        percent_change_1h = rate.percent_change_1h,
        percent_change_24h = rate.percent_change_24h) for rate in currency_rates]


@app.get("/latest_rate", response_model=CurrencyRatesBase)
async def get_latest_rate():
    return CurrencyRatesBase(
        currency = 1,
        date_added = datetime.datetime.now(),
        actual_date = datetime.datetime.now(),
        price_usd = 0.0,
        percent_change_1h = 0.0,
        percent_change_24h = 0.0)


@app.post("/create_rate")
async def create_new_rate(currency_rate: CurrencyRatesCreate, session: AsyncSession = Depends(get_session)):
    currency_rate = CurrencyRates(
        currency = None,#currency_rate.currency,
        date_added = currency_rate.date_added.replace(tzinfo=None) ,
        actual_date = currency_rate.actual_date.replace(tzinfo=None) ,
        price_usd = currency_rate.price_usd,
        percent_change_1h = currency_rate.percent_change_1h,
        percent_change_24h = currency_rate.percent_change_24h
    )
    session.add(currency_rate)
    await session.commit()
    await session.refresh(currency_rate)
    return currency_rate
