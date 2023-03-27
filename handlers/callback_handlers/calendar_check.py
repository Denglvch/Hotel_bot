from telebot.types import CallbackQuery

from handlers.message_handlers.calendar_start import calendar_start
from handlers.message_handlers.max_price_request import max_price_request
from loader import bot
from states.state_info import UserState


@bot.callback_query_handler(state=UserState.calendar_check, func=lambda call: call.data)
def calendar_check(call: CallbackQuery) -> None:
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        pass

    if data.get('date_out') and call.data == 'ok':
        bot.set_state(call.from_user.id, UserState.calendar_ok, call.message.chat.id)
        max_price_request(call)
    else:
        if call.data == 'rewrite':
            if data.get('date_out'):
                data['date_out'] = None
            else:
                data['date_in'] = None

        bot.set_state(call.from_user.id, UserState.city, call.message.chat.id)
        calendar_start(call)
