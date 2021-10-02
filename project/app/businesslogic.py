import datetime
import json
from typing import Any, Union
import aiohttp

from app.exceptions import IncorrectResponseData
from interfaces import DataAccessInterface
from config import settings
from app.models import CurrenciesCreate, CurrencyRatesCreate

class RequestCurrencyService():
    _data_access: DataAccessInterface

    def __init__(self, data_access: DataAccessInterface):
        self._data_access = data_access

    async def get_last_rate(self):
        return await self._data_access.async_get_last_currency_rate()

    async def get_list_rates(self):
        return await self._data_access.async_get_list_currency_rates()

    async def get_latest_rate(self, id: int) -> Union[CurrencyRatesCreate, None]:
        url: str = settings.url_api_foreign_service_rates
        api_key: dict = settings.api_key_service_rates
        params: dict = {
            **api_key,
            'id': id
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=params) as request:
                if request.status == 200:
                    result = await request.json()
                    decoded_data = await self._json_request_decode(data_json=result, id=id)
                    return await self._save_data(decoded_data)
        return None

    async def _json_request_decode(self, data_json: json, id: int) -> dict[str, dict[str, Union[int, Any]]]:
        try:
            result = {
                'currency': {
                    'id': id,
                    'name': data_json['data'][str(id)]['name'],
                    'slug': data_json['data'][str(id)]['slug'],
                    'symbol': data_json['data'][str(id)]['symbol'],
                },

                'currency_rate': {
                    'currency': id,
                    'actual_date': data_json['status']['timestamp'],
                    'price_usd': data_json['data'][str(id)]['quote']['USD']['price'],
                    'percent_change_1h': data_json['data'][str(id)]['quote']['USD']['percent_change_1h'],
                    'percent_change_24h': data_json['data'][str(id)]['quote']['USD']['percent_change_24h'],
                }
            }
        except KeyError:
            raise IncorrectResponseData("Incorrect JSON response")

        return result

    async def _save_data(self, data: dict[str, dict[str, Union[int, Any]]]) -> CurrencyRatesCreate:

        new_curency = CurrenciesCreate(
            id = data['currency']['id'],
            name = data['currency']['name'],
            slug = data['currency']['slug'],
            symbol = data['currency']['symbol']
        )

        new_curency_rate = CurrencyRatesCreate(
            currency = new_curency.id,
            date_added = datetime.datetime.now(),
            actual_date = data['currency_rate']['actual_date'],
            price_usd = data['currency_rate']['price_usd'],
            percent_change_1h = data['currency_rate']['percent_change_1h'],
            percent_change_24h = data['currency_rate']['percent_change_24h']
        )

        await self._data_access.async_create_currency(new_curency)
        await self._data_access.async_create_currency_rate(new_curency_rate)

        return new_curency_rate