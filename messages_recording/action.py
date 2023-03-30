from collections.abc import Callable
from contextlib import suppress

from telebot.apihelper import ApiTelegramException
from telebot.types import Message, CallbackQuery

from handlers.util_data import messages
from loader import bot


def add_to_messages(message: Message | CallbackQuery) -> None:
    """
    Adds a message ID and chat ID to the message store.
    :param message:
    """
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


def bot_send_message(*args, **kwargs) -> Message:
    """
    Wrapper function to catch bot messages.
    :param args:
    :param kwargs:
    """
    bot_msg: Message = bot.send_message(*args, disable_notification=True, **kwargs)
    add_to_messages(bot_msg)
    return bot_msg


def recording_msg(func: Callable) -> Callable:
    """
    Decorator to catch user messages.
    """
    def get_msg(message: Message | CallbackQuery):
        add_to_messages(message)
        func(message)
    return get_msg


def del_msg(chat_id: int) -> None:
    """
    Deletes previous messages in a dialog.
    :param chat_id:
    """
    if messages.get(chat_id):
        for message_id in messages.pop(chat_id):
            with suppress(ApiTelegramException):
                bot.delete_message(chat_id, message_id)

