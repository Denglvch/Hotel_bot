import functools
from collections.abc import Callable
from contextlib import suppress

from telebot.apihelper import ApiTelegramException
from telebot.types import Message, CallbackQuery

from database.db_read import messages_from_user
from database.db_write import db_add_message
from loader import bot


def bot_message_hook(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        bot_msg: Message = func(*args, **kwargs)
        db_add_message(bot_msg)
    return wrap


@bot_message_hook
def bot_send_message(*args, **kwargs):
    return bot.send_message(*args, **kwargs)


def recording_msg(func: Callable) -> Callable:
    def get_msg(message: Message | CallbackQuery):
        if isinstance(message, CallbackQuery):
            db_add_message(message.message)
            chat_id = message.message.chat.id
        else:
            db_add_message(message)
            chat_id = message.chat.id
        del_msg(chat_id)
        func(message)

    return get_msg


def del_msg(chat_id: int) -> None:
    messages = messages_from_user(chat_id=chat_id)
    for msg in messages:
        with suppress(ApiTelegramException):
            bot.delete_message(msg.chat_id, msg.message_id)

