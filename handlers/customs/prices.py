from telebot.types import CallbackQuery, Message

from handlers.customs.quantity import quantity_request
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


@bot.message_handler(state=UserState.min_price)
@recording_msg
def check_min_price(message: Message) -> None:
    del_msg(message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.isdigit():
            if int(message.text) <= data['max_price']:
                data['min_price'] = int(message.text)
                data['prices'] = {"max": data['max_price'],
                                  "min": data['min_price']}
                bot.set_state(message.from_user.id, UserState.check_price, message.chat.id)
                bot_send_message(message.from_user.id,
                                 'Напишите примелимое расстояние от отеля до центра в "км"'
                                 '\nЕсли это не важно, напишите 0 ')
            else:
                bot_send_message(message.from_user.id,
                                 'Минимальная цена не может быть больше максимальной :)')
        else:
            bot_send_message(message.from_user.id, 'Упс..'
                                                   '\nЧто то не так, давайте попробуем еще раз'
                                                   '\nИзбегайте любых символов кроме цифр'
                                                   '\nПример: 75')
