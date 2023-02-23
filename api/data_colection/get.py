from api.get_photo.get import take_photo


def get_collection(user_data: dict, hotel_list: list) -> list:
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
            photos = take_photo(hotel.get('id'), user_data['show_photo'])
            result = [text, photos]
            yield result
        else:
            yield text