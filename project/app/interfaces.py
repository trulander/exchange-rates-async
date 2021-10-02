from app.models import CurrenciesCreate, CurrencyRatesCreate, Currencies, CurrencyRates

class DataAccessInterface():
    async def async_create_currency(self, model: CurrenciesCreate) -> CurrenciesCreate:
        raise NotImplementedError('The method must be realized')

    async def async_get_currency_by_id(self, model: CurrenciesCreate) -> Currencies:
        raise NotImplementedError('The method must be realized')

    async def async_get_list_currencies(self, model: CurrenciesCreate) -> Currencies:
        raise NotImplementedError('The method must be realized')


    async def async_create_currency_rate(self, model: CurrencyRatesCreate) -> CurrencyRates:
        raise NotImplementedError('The method must be realized')

    async def async_get_last_currency_rate(self) -> CurrencyRates:
        raise NotImplementedError('The method must be realized')

    async def async_get_list_currency_rates(self) -> list[CurrencyRates]:
        raise NotImplementedError('The method must be realized')