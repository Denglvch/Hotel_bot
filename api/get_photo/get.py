from random import sample

from requests import request
from telebot.types import InputMediaPhoto
from api.api_data import api_data


def take_photo(hotel_id, amount_photo) -> list[InputMediaPhoto]:
    api_data.payload_mini['propertyId'] = hotel_id
    get_photo = request(
        "POST", f'{api_data.url.get("url")}{api_data.endpoints.get("detail")}',
        json=api_data.payload_mini,
        headers=api_data.headers.get('list')
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