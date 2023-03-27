from telebot.types import CallbackQuery

from handlers.message_handlers.quantity import quantity_request
from loader import bot
from messages_recording.action import recording_msg, del_msg, bot_send_message
from states.state_info import UserState


@bot.message_handler(state=UserState.calendar_ok)
@recording_msg
def max_price_request(call: CallbackQuery) -> None:
    del_msg(call.message.chat.id)
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        pass
    if data['command'] == 'bestdeal':
        bot.set_state(call.from_user.id, UserState.max_price, call.message.chat.id)
        bot_send_message(call.from_user.id, "Напишите максимальную цену для поиска"
                                            "\nПример: 250")
    else:
        bot.set_state(call.from_user.id, UserState.distance, call.message.chat.id)
        quantity_request(call)
