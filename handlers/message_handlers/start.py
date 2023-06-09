from telebot.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup

from database.db_write import db_add_user
from loader import bot
from messages_recording.action import recording_msg, del_msg, bot_send_message
from states.state_info import UserState


@bot.message_handler(commands=['start'])
@db_add_user
@recording_msg
def start(message: Message | CallbackQuery) -> None:
    """
    The main function of starting a dialog. Creates a keyboard with interaction options and sends it.
    :param message:
    :return: None
    """
    if isinstance(message, CallbackQuery):
        chat_id = message.message.chat.id
    else:
        chat_id = message.chat.id
    del_msg(chat_id)
    bot.reset_data(message.from_user.id, chat_id)
    lowprice = InlineKeyboardButton(text='Самые низкие цены', callback_data='lowprice')
    highprice = InlineKeyboardButton(text='Самые высокие цены', callback_data='highprice')
    bestdeal = InlineKeyboardButton(text='Лучшие цены по расположению', callback_data='bestdeal')
    history = InlineKeyboardButton(text='История поиска', callback_data='history')
    buttons = InlineKeyboardMarkup().add(lowprice, highprice, bestdeal, history, row_width=1)
    bot_send_message(chat_id, text='Что будем смотреть?', reply_markup=buttons)
    bot.set_state(message.from_user.id, UserState.start, chat_id)
