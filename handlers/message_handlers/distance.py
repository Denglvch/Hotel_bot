from telebot.types import Message

from handlers.message_handlers.quantity import quantity_request
from loader import bot
from messages_recording.action import recording_msg, del_msg, bot_send_message
from states.state_info import UserState


@bot.message_handler(state=UserState.check_price)
@recording_msg
def distance_request(message: Message) -> None:
    """
    Function validates the input in the previous step and redirects to the next or returns to the previous one.
    Also writes the necessary user data.
    :param message:
    :return: None
    """
    del_msg(message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.isdigit():
            data['distance'] = int(message.text)
            bot.set_state(message.from_user.id, UserState.distance, message.chat.id)
            quantity_request(message)
        else:
            bot_send_message(message.from_user.id, 'Упс..'
                                                   '\nЧто то не так, давайте попробуем еще раз'
                                                   '\nИзбегайте любых символов кроме цифр'
                                                   '\nПример: 75')
