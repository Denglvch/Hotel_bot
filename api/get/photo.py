from random import sample

from requests import request

from api.api_data import payload_mini, url, endpoints, headers


def get_photo(hotel_id: str, amount_photo: int) -> list:
    """
    Gets links to hotel photos.
    :param hotel_id:
    :param amount_photo:
    :return: List of links
    """
    payload_mini['propertyId'] = hotel_id
    photos = request(
        "POST", f'{url.get("url")}{endpoints.get("detail")}',
        json=payload_mini,
        headers=headers.get('list')
    ).json()

    all_img = photos['data']['propertyInfo']['propertyGallery']['images']
    return [
        img['image']['url']
        for img
        in sample(all_img, amount_photo)
    ]
