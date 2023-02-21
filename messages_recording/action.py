from loader import bot
from telebot.types import Message, CallbackQuery


def add_msg(func):
    def get_msg(message: Message | CallbackQuery):
        if isinstance(message, CallbackQuery):
            messages.append(message.message)
        else:
            messages.append(message)
        del_msg()
        return func(message)

    return get_msg


def del_msg():
    for msg in messages:
        if messages:
            try:
                bot.delete_message(msg.chat.id, msg.message_id)
            except:
                pass
    messages.clear()

messages: list = list()