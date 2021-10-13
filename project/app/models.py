from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field


class CurrencyBase(SQLModel):
    id: int
    name: str
    slug: str
    symbol: str


class Currency(CurrencyBase, table=True):
    id: int = Field(default=None, primary_key=True)


class CurrencyCreate(CurrencyBase):
    pass


class CurrencyRateBase(SQLModel):
    currency: Optional[int]
    date_added: datetime
    actual_date: datetime
    price_usd: Decimal
    percent_change_1h: float
    percent_change_24h: float


class CurrencyRate(CurrencyRateBase, table=True):
    id: int = Field(default=None, primary_key=True)
    currency: Optional[int] = Field(default=None, foreign_key='currency.id')


class CurrencyRateCreate(CurrencyRateBase):
    pass