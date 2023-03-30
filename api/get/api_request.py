from requests import request
from api.api_data import url, endpoints, headers, querystring, payload


def get_api_request() -> dict:
    """
    Common function for making request to API
    :return: Response
    """
    city_search = request(
        "GET", f'{url.get("url")}{endpoints.get("search")}',
        headers=headers.get("search"), params=querystring
    ).json()

    payload["destination"]["regionId"] = city_search.get('sr')[0].get('gaiaId')

    hotels = request(
        "POST", f'{url.get("url")}{endpoints.get("list")}',
        json=payload, headers=headers.get("list")
    ).json()

    return hotels
