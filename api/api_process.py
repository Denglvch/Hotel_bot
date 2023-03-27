from telebot.types import InputMediaPhoto

from api.api_data import check_in_out, querystring, payload
from api.filter import filter_by_distance
from api.get import api_request, collection
from database.db_write import db_add_response


@db_add_response
def process(user_data=None) -> list[str | list[InputMediaPhoto]] | list[str] | str:

    if user_data is None:
        user_data = dict()
    check_in_out['date_in'], check_in_out['date_out'] = user_data['date_in'], user_data['date_out']
    querystring["q"]: str = user_data['city']
    payload["filters"]["price"]: dict = user_data['price_in']
    low_to_high: bool = user_data['command'] == 'highprice'

    city_request: dict = api_request.get_api_request()

    if city_request.get('data'):
        hotel_list: list = city_request['data']['propertySearch']['properties']
        if user_data.get('distance', 0):
            hotel_list: list = filter_by_distance(hotel_list, user_data.get('distance'))
        if low_to_high:
            hotel_list: list = hotel_list[:user_data['quantity']]
        else:
            hotel_list: list = hotel_list[:-(user_data['quantity'] + 1):-1]

        return [
            result
            for result
            in collection.get_collection(user_data, hotel_list)
        ]

    else:
        return (':('
                '\nС такими параметрами ничего не нашлось.'
                '\nПопробуйте изменить параметры')
