from telebot.types import InputMediaPhoto

from api.get.photo import get_photo
from database.db_write import db_add_response


@db_add_response
def create_collection(user_data: dict, text: str = None, photo_links: list = None, in_db=False) -> list | str:
    if photo_links:
        mediagroup = [
            InputMediaPhoto(media=photo)
            for photo
            in photo_links
        ]
        return [text, mediagroup]
    return text


def get_collection(user_data: dict, hotel_list: list) -> list | str:
    all_days = (user_data['date_out'] - user_data['date_in']).days
    for hotel in hotel_list:
        name = hotel['name']
        price: str = hotel['price']['lead']['formatted']
        distance = hotel['destinationInfo']['distanceFromDestination']['value']
        text = (f'\nОтель: {name}'
                f'\nЦена за ночь: {price}'
                f'\nЦена за {all_days} ночей: {all_days * int(price.lstrip("$"))}'
                f'\nРасстояние до центра: {distance} км')
        if user_data['show_photo']:
            photos = get_photo(hotel.get('id'), user_data['show_photo'])
            yield create_collection(user_data, text=text, photo_links=photos)
            # result = [text, photos]
            # yield result
        else:
            yield create_collection(user_data, text=text)
