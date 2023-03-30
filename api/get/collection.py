from telebot.types import InputMediaPhoto

from api.get.photo import get_photo
from database.db_write import db_add_response


@db_add_response
def create_collection(
        user_data=None,
        text: str = None,
        photo_links: list = None,
        in_db=False
) -> list | str:
    """
    If there are photos, converts them to an InputMediaPhoto object.
    :param user_data:
    :param text:
    :param photo_links:
    :param in_db:
    :return: list or text with hotel information
    """
    if user_data is None:
        user_data = dict()
    if photo_links:
        mediagroup = [
            InputMediaPhoto(media=photo)
            for photo
            in photo_links
        ]
        return [text, mediagroup]
    return text


def get_collection(user_data: dict, hotel_list: list) -> list | str:
    """
        Collects and groups information about hotels.
    :param user_data:
    :param hotel_list:
    :return: list or text with hotel information
    """
    all_days = (user_data['date_out'] - user_data['date_in']).days
    for hotel in hotel_list:
        name: str = hotel['name']
        price: str = hotel['price']['lead']['formatted']
        distance = hotel['destinationInfo']['distanceFromDestination']['value']
        text = (f'\nОтель: {name}'
                f'\nЦена за ночь: {price}'
                f'\nЦена за {all_days} ночей: {all_days * int(price.lstrip("$"))}'
                f'\nРасстояние до центра: {distance} км')
        if user_data['show_photo']:
            photos = get_photo(hotel.get('id'), user_data['show_photo'])
            yield create_collection(user_data=user_data, text=text, photo_links=photos)
        else:
            yield create_collection(user_data=user_data, text=text)
