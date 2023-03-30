from telebot.types import CallbackQuery

from handlers.util_data import text_command
from loader import bot
from messages_recording.action import recording_msg, del_msg, bot_send_message
from states.state_info import UserState


@bot.callback_query_handler(state=UserState.start, func=lambda call: call.data != 'history')
@recording_msg
def city_request(call: CallbackQuery) -> None:
    """
    The function sends a message to the user with an invitation to enter the name of the city,
    and also writes the necessary user data.
    :param call:
    :return: None
    """
    del_msg(call.message.chat.id)
    bot.set_state(call.from_user.id, UserState.city, call.message.chat.id)
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['user_id'] = call.from_user.id
        data['command'] = call.data
        data['text_command'] = text_command[call.data]
    bot_send_message(call.from_user.id, "Введите название города,\nНапример: new york")
