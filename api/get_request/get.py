from requests import request
from api.api_data import api_data


def make_request() -> dict:
    city_search = request(
        "GET", f'{api_data.url.get("url")}{api_data.endpoints.get("search")}',
        headers=api_data.headers.get("search"), params=api_data.querystring
    ).json()
    # print(city_search.status_code)

    api_data.payload["destination"]["regionId"] = city_search.get('sr')[0].get('gaiaId')

    hotels = request(
        "POST", f'{api_data.url.get("url")}{api_data.endpoints.get("list")}',
        json=api_data.payload, headers=api_data.headers.get("list")
    ).json()
    # print(hotel_search.status_code)

    return hotels