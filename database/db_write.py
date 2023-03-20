from collections.abc import Callable
from json import dumps

from telebot.types import Message, CallbackQuery

from database.models import User, UserRequest


def db_add_user(func) -> Callable:
    def add(message: Message | CallbackQuery) -> None:
        find_user = User.select().limit(1).where(User.user_id == message.from_user.id)
        check_user = [
            user.user_id
            for user
            in find_user
        ]
        if not check_user:
            User(user_id=message.from_user.id).save()
        return func(message)
    return add


def db_add_response(func: Callable) -> Callable:
    def add(*args, **kwargs) -> list:
        result = None
        if func.__name__ == 'process':
            result = func(*args, **kwargs)
            kwargs['in_db'] = True

        user_data: dict = args[0]
        if user_data.get('command') != 'history':
            if kwargs.get('in_db'):
                data = dumps(
                    {'response': user_data.get('response')},
                    ensure_ascii=False
                )
                # user = User.get(user_id=user_data['user_id'])
                UserRequest(
                    user_id=User.get(user_id=user_data['user_id']),
                    text=user_data['text_response'],
                    request=data
                ).save()
            else:
                if kwargs.get('photo_links'):
                    data_in = [kwargs['text'], kwargs.get('photo_links')]
                else:
                    data_in = kwargs['text']
                user_data.get(
                    'response',
                    user_data.update({'response': list()})
                ).append(data_in)

        return result or func(*args, **kwargs)
    return add
