from collections.abc import Callable
from json import dumps

from telebot.types import Message, CallbackQuery

from database.models import User, UserRequest, UserMessage


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


def db_add_message(message: Message | CallbackQuery) -> None:

    if isinstance(message, CallbackQuery):
        chat_id = message.message.chat.id
        message_id = message.message.message_id
    else:
        chat_id = message.chat.id
        message_id = message.message_id
    UserMessage(
        user_id=User.get(user_id=message.from_user.id),
        chat_id=chat_id,
        message_id=message_id
    ).save()


def db_add_response(func: Callable) -> Callable:
    def add(*args, **kwargs) -> Callable:
        result = None
        if func.__name__ == 'process':
            result = func(*args, **kwargs)
            kwargs['in_db'] = True

        user_data: dict = kwargs['user_data']
        if user_data.get('command') != 'history':
            if kwargs.get('in_db'):
                data = dumps(
                    {'response': user_data.get('response')},
                    ensure_ascii=False
                )
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
                if not user_data.get('response'):
                    user_data.update({'response': list()})
                user_data.get('response').append(data_in)
        return result or func(*args, **kwargs)
    return add
