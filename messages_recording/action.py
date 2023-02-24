from telebot.apihelper import ApiTelegramException

from loader import bot
from telebot.types import Message, CallbackQuery
from contextlib import suppress
from collections.abc import Callable


def recording_msg(func: Callable) -> Callable:
    def get_msg(message: Message | CallbackQuery):
        if isinstance(message, CallbackQuery):
            messages.append(message.message)
        else:
            messages.append(message)
        del_msg()
        func(message)

    return get_msg


def del_msg() -> None:
    for msg in messages:
        with suppress(ApiTelegramException):
            bot.delete_message(msg.chat.id, msg.message_id)
    messages.clear()


messages: list = list()
