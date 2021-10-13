from app.models import CurrencyCreate, CurrencyRateCreate, Currency, CurrencyRate

class DataAccessInterface():
    async def async_create_currency(self, model: CurrencyCreate) -> CurrencyCreate:
        raise NotImplementedError('The method must be realized')

    async def async_get_currency_by_id(self, model: CurrencyCreate) -> Currency:
        raise NotImplementedError('The method must be realized')

    async def async_get_list_currencies(self, model: CurrencyCreate) -> Currency:
        raise NotImplementedError('The method must be realized')


    async def async_create_currency_rate(self, model: CurrencyRateCreate) -> CurrencyRate:
        raise NotImplementedError('The method must be realized')

    async def async_get_last_currency_rate(self) -> CurrencyRate:
        raise NotImplementedError('The method must be realized')

    async def async_get_list_currency_rates(self) -> list[CurrencyRate]:
        raise NotImplementedError('The method must be realized')