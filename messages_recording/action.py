import functools
from collections.abc import Callable
from contextlib import suppress

from telebot.apihelper import ApiTelegramException
from telebot.types import Message, CallbackQuery

from handlers.util_data import messages
from loader import bot


def add_to_messages(message: Message | CallbackQuery) -> None:
    if isinstance(message, CallbackQuery):
        message_id = message.message.id
        chat_id = message.message.chat.id
    else:
        message_id = message.id
        chat_id = message.chat.id
    if messages.get(chat_id):
        messages[chat_id].append(message_id)
    else:
        messages[chat_id] = [message_id]


def bot_message_hook(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrap(*args, **kwargs) -> None:
        bot_msg: Message = func(*args, **kwargs)
        add_to_messages(bot_msg)
    return wrap


@bot_message_hook
def bot_send_message(*args, **kwargs) -> Message:
    return bot.send_message(*args, disable_notification=True, **kwargs)


def recording_msg(func: Callable) -> Callable:
    def get_msg(message: Message | CallbackQuery):
        add_to_messages(message)
        func(message)
    return get_msg


def del_msg(chat_id: int) -> None:
    if messages.get(chat_id):
        for message_id in messages.pop(chat_id):
            with suppress(ApiTelegramException):
                bot.delete_message(chat_id, message_id)

