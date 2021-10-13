from app.models import CurrencyRateCreate, CurrencyCreate, CurrencyRate, Currency
from app.interfaces import DataAccessInterface
from app.db import async_session

from sqlalchemy.future import select
from sqlalchemy.sql.expression import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import Insert

class DataAccess(DataAccessInterface):
    _db_session: AsyncSession

    def __init__(self):
        self._db_session = async_session

    async def async_create_currency(self, model: CurrencyCreate) -> CurrencyCreate:
        await self._db_session.execute(Insert(Currency).values({
                "id": model.id,
                "name": model.name,
                "slug": model.slug,
                "symbol": model.symbol
             }).on_conflict_do_nothing())
        await self._db_session.commit()
        return model

    # async def async_get_currency_by_id(self, model: CurrencyCreate) -> bool:
    #     pass
    #
    # async def async_get_list_currencies(self, model: CurrencyCreate) -> bool:
    #     pass



    async def async_create_currency_rate(self, model: CurrencyRateCreate) -> CurrencyRate:
        currency_rate = CurrencyRate(
            currency = model.currency,
            date_added = model.date_added.replace(tzinfo=None),
            actual_date = model.actual_date.replace(tzinfo=None),
            price_usd = model.price_usd,
            percent_change_1h = model.percent_change_1h,
            percent_change_24h = model.percent_change_24h
        )
        self._db_session.add(currency_rate)
        await self._db_session.commit()
        await self._db_session.refresh(currency_rate)
        return currency_rate

    async def async_get_last_currency_rate(self) -> CurrencyRate:
        request = await self._db_session.execute(select(CurrencyRate).order_by(desc(CurrencyRate.id)))
        result = request.scalars().first()
        return result

    async def async_get_list_currency_rates(self) -> list[CurrencyRate]:
        result = await self._db_session.execute(select(CurrencyRate))
        currency_rates: list[CurrencyRate] = result.scalars().all()
        return [rate for rate in currency_rates]


