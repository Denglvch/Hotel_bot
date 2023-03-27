from telebot.types import Message

from loader import bot
from messages_recording.action import recording_msg, del_msg, bot_send_message
from states.state_info import UserState


@bot.message_handler(state=UserState.max_price)
@recording_msg
def min_price_request(message: Message) -> None:
    del_msg(message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.isdigit():
            data['max_price'] = int(message.text)
            bot.set_state(message.from_user.id, UserState.min_price, message.chat.id)
            bot_send_message(message.from_user.id, "Напишите минимальную цену для поиска"
                                                   "\nПример: 75")
        else:
            bot_send_message(message.from_user.id, 'Упс..'
                                                   '\nЧто то не так, давайте попробуем еще раз'
                                                   '\nИзбегайте любых символов кроме цифр'
                                                   '\nПример: 75')
