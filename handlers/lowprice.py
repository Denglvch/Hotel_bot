from loader import bot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

import api
from states.state_info import UserState
from messages_recording.action import recording_msg, del_msg, messages
from pagination.switch import switch

prices = {'/lowprice': {'max': 100,
                        'min': 1},
          '/highprice': {'max': 9999,
                         'min': 100},
          }


@bot.callback_query_handler(func=lambda call: call.data == 'start')
@recording_msg
def call_start(call: CallbackQuery):
    start(call.message)


@bot.message_handler(commands=['start'])
@recording_msg
def start(message: Message):

    lowprice = InlineKeyboardButton(text='Самые низкие цены', callback_data='lowprice')
    highprice = InlineKeyboardButton(text='Самые высокие цены', callback_data='highprice')
    bestdeal = InlineKeyboardButton(text='Лучшие цены по расположению', callback_data='bestdeal')
    markup = InlineKeyboardMarkup().add(lowprice, highprice, bestdeal, row_width=1)
    msg = bot.send_message(message.chat.id, text='Что будем смотреть?', reply_markup=markup)
    messages.append(msg)


@bot.callback_query_handler(func=lambda call: call.data in ['lowprice', 'highprice', 'bestdeal'])
# @bot.message_handler(handlers=['lowprice', 'highprice', 'bestdeal'])
@recording_msg
def city_request(call: CallbackQuery):
    del_msg()
    bot.reset_data(call.from_user.id, call.message.id)
    bot.set_state(call.from_user.id, UserState.city, call.message.chat.id)
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['command'] = call.data
    msg = bot.send_message(call.from_user.id, "Введите название города")
    messages.append(msg)


@bot.message_handler(state=UserState.city)
@recording_msg
def max_price_request(message):
    del_msg()
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text
        if data['command'] == 'bestdeal':
            bot.set_state(message.from_user.id, UserState.max_price, message.chat.id)
            msg = bot.send_message(message.from_user.id, "Напишите максимальную цену для поиска"
                                                         "\nПример: 250")
            messages.append(msg)
        else:
            bot.set_state(message.from_user.id, UserState.distance, message.chat.id)
            quantity_request(message)


@bot.message_handler(state=UserState.max_price)
@recording_msg
def min_price_request(message):
    del_msg()
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.isdigit():
            data['max_price'] = int(message.text)
            bot.set_state(message.from_user.id, UserState.min_price, message.chat.id)
            msg = bot.send_message(message.from_user.id, "Напишите минимальную цену для поиска"
                                                         "\nПример: 75")
            messages.append(msg)
        else:
            msg = bot.send_message(message.from_user.id, 'Упс..'
                                                         '\nЧто то не так, давайте попробуем еще раз')
            messages.append(msg)


@bot.message_handler(state=UserState.min_price)
@recording_msg
def check_min_price(message):
    del_msg()
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.isdigit():
            if int(message.text) <= data['max_price']:
                data['min_price'] = int(message.text)
                data['prices'] = {"max": data['max_price'],
                                  "min": data['min_price']}
                bot.set_state(message.from_user.id, UserState.check_price, message.chat.id)
                msg = bot.send_message(message.from_user.id,
                                       'Напишите примелимое расстояние от отеля до центра в "км"'
                                       '\nЕсли это не важно, напишите 0 ')
                messages.append(msg)
            else:
                msg = bot.send_message(message.from_user.id,
                                       'Минимальная цена не может быть больше максимальной :)')
                messages.append(msg)
        else:
            msg = bot.send_message(message.from_user.id, 'Упс..'
                                                         '\nЧто то не так, давайте попробуем еще раз')
            messages.append(msg)


@bot.message_handler(state=UserState.check_price)
@recording_msg
def distance_request(message):
    del_msg()
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.isdigit():
            data['distance'] = int(message.text)
            bot.set_state(message.from_user.id, UserState.distance, message.chat.id)
            quantity_request(message)
        else:
            msg = bot.send_message(message.from_user.id, 'Упс..'
                                                         '\nЧто то не так, давайте попробуем еще раз')
            messages.append(msg)


@bot.message_handler(state=UserState.distance)
@recording_msg
def quantity_request(message):
    del_msg()
    bot.set_state(message.from_user.id, UserState.quantity, message.chat.id)
    msg = bot.send_message(message.from_user.id, "Сколько отелей показать?")
    messages.append(msg)


@bot.message_handler(state=UserState.quantity)
@recording_msg
def show_photo(message):
    del_msg()
    bot.set_state(message.from_user.id, UserState.show_photo, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['quantity'] = int(message.text)
    msg = bot.send_message(message.from_user.id, "Сколько фото показать по каждому отелю?"
                                                 "\nЕсли фото не нужны введите 0?")
    messages.append(msg)


@bot.message_handler(state=UserState.show_photo)
@recording_msg
def reply(message):
    del_msg()
    check = False
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.isdigit():
            data['show_photo'] = int(message.text)
            check = True
        else:
            msg = bot.send_message(message.from_user.id, 'Упс..'
                                                         '\nЧто то не так, давайте попробуем еще раз')
            messages.append(msg)
    if check:
        msg = bot.send_message(message.chat.id, 'Минуточку...')
        messages.append(msg)
        price_in = prices.get(data['command'], data.get('prices'))
        get_result = api.top_price.get_top(data, price_in)
        # if data['show_photo']:
        #     for msg in get_result:
        #         messages.append(msg)

        switch(message, get_result)

