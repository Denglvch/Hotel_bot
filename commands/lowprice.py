from typing import Any

from states.state_info import UserState
from typing import Any
import api


def bot_load(bot: Any):
    @bot.message_handler(commands=['lowprice'])
    def city_request(message):
        bot.set_state(message.from_user.id, UserState.city, message.chat.id)
        bot.send_message(message.from_user.id, "Введите название города")

    @bot.message_handler(state=UserState.city)
    def quantity_request(message):
        bot.set_state(message.from_user.id, UserState.quantity, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text
        bot.send_message(message.from_user.id, "Сколько отелей показать?")

    @bot.message_handler(state=UserState.quantity)
    def reply(message):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['quantity'] = message.text
        bot.send_message(message.chat.id, 'Минуточку...')
        bot.send_message(message.chat.id, api.lowprice_req.get(data['quantity'], data['city']))
