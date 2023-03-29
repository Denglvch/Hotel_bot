from json import loads as json_loads

from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from database.db_read import search_history
from loader import bot
from messages_recording.action import recording_msg, bot_send_message, del_msg
from states.state_info import UserState


@bot.callback_query_handler(state=UserState.start, func=lambda call: call.data == 'history')
@recording_msg
def history_check(call: CallbackQuery) -> None:
    del_msg(call.message.chat.id)
    db_response = search_history(call)
    if db_response:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['command'] = call.data
            data['history'] = {
                str(num): json_loads(old.request)
                for num, old
                in enumerate(db_response, 1)
            }
        buttons = [
            InlineKeyboardButton(text=resp.text, callback_data=str(num))
            for num, resp
            in enumerate(db_response, 1)
        ]
        keyboard = InlineKeyboardMarkup().add(*buttons, row_width=1)
        bot.set_state(call.from_user.id, UserState.history_look, call.message.chat.id)
        bot_send_message(call.message.chat.id, text='Выберите запрос для просмотра', reply_markup=keyboard)

    else:
        bot.set_state(call.from_user.id, UserState.switch, call.message.chat.id)
        keyboard = InlineKeyboardMarkup().add((InlineKeyboardButton('Меню бота', callback_data='start')))
        bot_send_message(call.message.chat.id, 'В истории пока ничего нет.\nПопробуйте сделать первый запрос)',
                         reply_markup=keyboard)
