
from requests import request
from datetime import date, timedelta
from config import config
from random import sample
from telebot.types import InputMediaPhoto


def filter_by_distance(data: list, distance: int) -> list:
    return [hotel
            for hotel
            in data
            if hotel['destinationInfo']['distanceFromDestination']['value'] <= distance
            ]


def make_request() -> dict:
    city_search = request(
        "GET", f'{url.get("url")}{endpoints.get("search")}',
        headers=headers.get("search"), params=querystring
    ).json()
    # print(city_search.status_code)

    payload["destination"]["regionId"] = city_search.get('sr')[0].get('gaiaId')

    hotels = request(
        "POST", f'{url.get("url")}{endpoints.get("list")}',
        json=payload, headers=headers.get("list")
    ).json()
    # print(hotel_search.status_code)

    return hotels


def take_photo(hotel_id, amount_photo) -> list[InputMediaPhoto]:
    payload_mini['propertyId'] = hotel_id
    get_photo = request(
        "POST", f'{url.get("url")}{endpoints.get("detail")}',
        json=payload_mini,
        headers=headers.get('list')
    ).json()

    all_img = get_photo['data']['propertyInfo']['propertyGallery']['images']
    list_of_links = [
        img['image']['url']
        for img
        in sample(all_img, amount_photo)
    ]

    return [
        InputMediaPhoto(media=photo)
        for photo
        in list_of_links
    ]


def get_collection(user_data: dict, hotel_list: list) -> list:
    for hotel in hotel_list:
        name = hotel['name']
        price = hotel['price']['lead']['formatted']
        distance = hotel['destinationInfo']['distanceFromDestination']['value']
        text = (f'\nОтель: {name}'
                f'\nЦена за ночь: {price}'
                f'\nРасстояние до центра: {distance} км')
        if user_data['show_photo']:
            photos = take_photo(hotel.get('id'), user_data['show_photo'])
            result = [text, photos]
            yield result
        else:
            yield text


def get_top(user_data: dict, price_in: dict) -> list[str | list[InputMediaPhoto]] | list[str] | str:

    querystring["q"]: str = user_data['city']
    payload["filters"]["price"]: dict = price_in
    low_to_high: bool = user_data['command'] == 'highprice'

    data: dict = make_request()

    if data.get('data'):
        hotel_list: list = data['data']['propertySearch']['properties']
        # print('len', len(hotel_list))
        if user_data.get('distance', 0):
            hotel_list: list = filter_by_distance(hotel_list, user_data.get('distance'))

        if low_to_high:
            hotel_list: list = hotel_list[:user_data['quantity']]
        else:
            hotel_list: list = hotel_list[:-(user_data['quantity'] + 1):-1]
        try:
            # print(len(hotel_list))
            return [
                result
                for result
                in get_collection(user_data, hotel_list)
            ]
        except IndexError:
            print("D'oh!")
        # return '\n'.join(result)
    else:
        return (':('
                '\nС такими параметрами ничего не нашлось.'
                '\nПопробуйте изменить параметры')


today = date.today()
tomorrow = today + timedelta(days=1)

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
        "day": today.day,
        "month": today.month,
        "year": today.year},
    "checkOutDate": {
        "day": tomorrow.day,
        "month": tomorrow.month,
        "year": tomorrow.year},
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
