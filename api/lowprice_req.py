import json
import requests
from config import config


def get(amount: str, city: str, min_price: int = 1, max_price: int = 100) -> str:
    amount = int(amount)

    url = "https://hotels4.p.rapidapi.com/"

    endpoints = {'search': 'locations/v3/search',
                 'list': 'properties/v2/list'}

    querystring = {"q": city, "locale": "ru_RU", "langid": "1033", "siteid": "300000001"}

    headers = {
        'search':
            {"X-RapidAPI-Key": config.get('api_key'),
             "X-RapidAPI-Host": "hotels4.p.rapidapi.com"},
        'list':
            {"content-type": "application/json",
             "X-RapidAPI-Key": config.get('api_key'),
             "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}
    }

    response = requests.request(
        "GET", f'{url}{endpoints.get("search")}',
        headers=headers.get("search"), params=querystring
    )

    data = json.loads(response.text)
    rid = data.get('rid')

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": rid},
        "checkInDate": {
            "day": 26,
            "month": 12,
            "year": 2022
        },
        "checkOutDate": {
            "day": 27,
            "month": 12,
            "year": 2022
        },
        "rooms": [
            {
                "adults": 2,
                "children": [{"age": 5}, {"age": 7}]
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": amount,
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {"price": {
            "max": max_price,
            "min": min_price
        }}
    }

    response = requests.request(
        "POST", f'{url}{endpoints.get("list")}',
        json=payload, headers=headers.get("list")
    )

    data = json.loads(response.text)
    # print(data)

    hotel_list = data['data']['propertySearch']['properties']

    result = list()
    try:
        for hotel in hotel_list:
            name = hotel['name']
            price = hotel['price']['lead']['formatted']
            result.append(f'\n{name}'
                          f'\n{price}')
    except IndexError:
        print("D'oh!")
    return '\n'.join(result)
