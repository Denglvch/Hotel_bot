from telebot.types import InputMediaPhoto
from api.api_data import api_data
from api.get_request import get
from api.filters.filter import filter_by_distance
from api.data_colection.get import get_collection


def get_top(user_data: dict, price_in: dict) -> list[str | list[InputMediaPhoto]] | list[str] | str:

    api_data.check_in_out['date_in'], api_data.check_in_out['date_out'] = user_data['date_in'], user_data['date_out']
    api_data.querystring["q"]: str = user_data['city']
    api_data.payload["filters"]["price"]: dict = price_in
    low_to_high: bool = user_data['command'] == 'highprice'

    data: dict = get.make_request()

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