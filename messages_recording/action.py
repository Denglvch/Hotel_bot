import functools
from collections.abc import Callable
from contextlib import suppress

from telebot.apihelper import ApiTelegramException
from telebot.types import Message, CallbackQuery

from handlers.util_data import messages
from loader import bot


def bot_message_hook(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrap(*args, **kwargs) -> None:
        bot_msg: Message = func(*args, **kwargs)
        messages.append(bot_msg)
    return wrap


@bot_message_hook
def bot_send_message(*args, **kwargs) -> Message:
    return bot.send_message(*args, disable_notification=True, **kwargs)


def recording_msg(func: Callable) -> Callable:
    def get_msg(message: Message | CallbackQuery):
        if isinstance(message, CallbackQuery):
            messages.append(message.message)
            chat_id = message.message.chat.id
        else:
            messages.append(message)
            chat_id = message.chat.id
        del_msg(chat_id)
        func(message)

    return get_msg


def del_msg(chat_id: int) -> None:
    for msg in messages:
        if isinstance(msg, CallbackQuery):
            chat = msg.message.chat.id
            message_id = msg.message.id
        else:
            chat = msg.chat.id
            message_id = msg.id
        if chat_id == chat:
            with suppress(ApiTelegramException):
                bot.delete_message(chat_id, message_id)

