from random import sample

from requests import request
from telebot.types import InputMediaPhoto
from api.api_data import payload_mini, url, endpoints, headers


def get_photo(hotel_id: str, amount_photo: int) -> list[InputMediaPhoto]:
    payload_mini['propertyId'] = hotel_id
    photos = request(
        "POST", f'{url.get("url")}{endpoints.get("detail")}',
        json=payload_mini,
        headers=headers.get('list')
    ).json()

    all_img = photos['data']['propertyInfo']['propertyGallery']['images']
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