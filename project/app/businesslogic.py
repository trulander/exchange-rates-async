import json
from typing import Any, Union, Dict
import aiohttp


from Core.Exceptions.exceprions import IncorrectResponseData, InvalidateSerializerData
from services.serializers import CurrencyRatesSerializer, CurrenciesSerializer





from interfaces import DataAccessInterface

class RequestCurrencyService():
    def __init__(self,
                 data_access: DataAccessInterface,):


    def request(self, id: int) -> Union[Dict, None]:
        url: str = settings.URL_API_GET_ACTUALL_CURRENCY
        api_key: dict = settings.API_KEY
        params: dict = {
            **api_key,
            'id': id
        }

        result: Response = requests.get(url=url, params=params)
        if result.status_code == 200:
            decoded_data = self._json_request_decode(data_json=result.json(), id=id)
            return self._save_data(decoded_data)

        return None

    def _json_request_decode(self, data_json: json, id: int) -> dict[str, dict[str, Union[int, Any]]]:
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

    def _save_data(self, data: dict[str, dict[str, Union[int, Any]]]) -> json:
        currency_serializer = CurrenciesSerializer(data=data['currency'])
        currency_rate_serializer = CurrencyRatesSerializer(data=data['currency_rate'])

        if currency_serializer.is_valid():
            currency_serializer.save()

        if currency_rate_serializer.is_valid():
            currency_rate_serializer.save()
        else:
            raise InvalidateSerializerData(currency_rate_serializer.errors)

        return currency_rate_serializer.data
