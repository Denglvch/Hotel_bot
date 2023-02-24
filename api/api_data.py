from datetime import datetime
from config import config

check_in_out = {'date_in': datetime.today(),
                'date_out': datetime.today()}

url: dict = {'url': "https://hotels4.p.rapidapi.com/"}

endpoints: dict = {'search': 'locations/v3/search',
                   'list': 'properties/v2/list',
                   'detail': 'properties/v2/detail'}

querystring: dict = {"q": 'new york', "locale": "ru_RU", "langid": "1033", "siteid": "300000001"}

headers: dict = {
    'search':
        {"X-RapidAPI-Key": config.get('api_key'),
         "X-RapidAPI-Host": "hotels4.p.rapidapi.com"},
    'list':
        {"content-type": "application/json",
         "X-RapidAPI-Key": config.get('api_key'),
         "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}
}

payload_mini: dict = {
    "currency": "USD",
    "eapid": 1,
    "locale": "en_US",
    "siteId": 300000001,
    "propertyId": "9209612"
}

payload: dict = {
    "currency": "USD",
    "eapid": 1,
    "locale": "en_US",
    "siteId": 300000001,
    "destination": {"regionId": 6054439},
    "checkInDate": {
        "day": check_in_out.get('date_in').day,
        "month": check_in_out.get('date_in').month,
        "year": check_in_out.get('date_in').year},
    "checkOutDate": {
        "day": check_in_out.get('date_out').day,
        "month": check_in_out.get('date_out').month,
        "year": check_in_out.get('date_out').year},
    "rooms": [
        {
            "adults": 2,
            "children": []
        }
    ],
    "resultsStartingIndex": 0,
    "resultsSize": 1000,
    "sort": "PRICE_LOW_TO_HIGH",
    "filters": {"price": {
        "max": 100,
        "min": 1
    }}
}
