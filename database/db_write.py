from collections.abc import Callable

from peewee import *
from telebot.types import Message, CallbackQuery, InputMediaPhoto

from database.models import db, User, UserRequest
from json import dumps


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


def db_add_response(func) -> Callable:
    def add(*args, **kwargs) -> list[str | list[InputMediaPhoto]] | list[str] | str:
        response = func(*args, **kwargs)
        data = dumps({'response': response})
        user = User.get(user_id=kwargs['user_id'])
        UserRequest(user_id=user, request=data).save()
        return response
    return add
