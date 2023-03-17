from database.db_write import db_add_user
from loader import bot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from api.api_process import process
from states.state_info import UserState
from messages_recording.action import recording_msg, del_msg, messages
from pagination.switch import switch
from datetime import date

prices = {
    '/lowprice': {'max': 100,
                  'min': 1},
    '/highprice': {'max': 9999,
                   'min': 100},
}

ru_steps = {
    'year': 'год',
    'month': 'месяц',
    'day': 'день'
}


def markup(photo: bool = False) -> InlineKeyboardMarkup:
    keyboard = [
        InlineKeyboardButton(text=num, callback_data=num)
        for num
        in range(3, 11)
    ]
    buttons = InlineKeyboardMarkup().add(*keyboard, row_width=8)
    if photo:
        no_photo = InlineKeyboardButton(text='Без фото', callback_data='0')
        buttons.add(no_photo)

    return buttons


@bot.callback_query_handler(state=UserState.switch, func=lambda call: call.data == 'start')
def callback_start(call: CallbackQuery) -> None:
    start(call)


@bot.message_handler(commands=['start'])
@db_add_user
@recording_msg
def start(message: Message | CallbackQuery) -> None:
    if isinstance(message, CallbackQuery):
        chat_id = message.message.chat.id
    else:
        chat_id = message.chat.id
    bot.reset_data(message.from_user.id, chat_id)
    lowprice = InlineKeyboardButton(text='Самые низкие цены', callback_data='lowprice')
    highprice = InlineKeyboardButton(text='Самые высокие цены', callback_data='highprice')
    bestdeal = InlineKeyboardButton(text='Лучшие цены по расположению', callback_data='bestdeal')
    buttons = InlineKeyboardMarkup().add(lowprice, highprice, bestdeal, row_width=1)
    msg = bot.send_message(chat_id, text='Что будем смотреть?', reply_markup=buttons)
    bot.set_state(message.from_user.id, UserState.start, chat_id)
    messages.append(msg)


@bot.callback_query_handler(state=UserState.start, func=lambda call: call.data)
@recording_msg
def city_request(call: CallbackQuery) -> None:
    del_msg()

    bot.set_state(call.from_user.id, UserState.city, call.message.chat.id)
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['command'] = call.data
    msg = bot.send_message(call.from_user.id, "Введите название города")
    messages.append(msg)


@bot.message_handler(state=UserState.city)
@recording_msg
def calendar_start(message: Message | CallbackQuery) -> None:
    if isinstance(message, CallbackQuery):
        chat_id = message.message.chat.id
    else:
        chat_id = message.chat.id
    with bot.retrieve_data(message.from_user.id, chat_id) as data:
        if not data.get('city'):
            data['city'] = message.text
        if data.get('date_in'):
            data['move'] = 'выезда'
        else:
            data['move'] = 'заезда'
    del_msg()
    bot.set_state(message.from_user.id, UserState.calendar_start, chat_id)
    calendar_obj = DetailedTelegramCalendar(min_date=date.today())
    calendar, step = calendar_obj.build()
    msg = bot.send_message(
        chat_id,
        f"Выберите {ru_steps[LSTEP[step]]} {data['move']}",
        reply_markup=calendar
    )
    messages.append(msg)


@bot.callback_query_handler(state=UserState.calendar_start, func=DetailedTelegramCalendar.func())
def calendar_steps(call: CallbackQuery) -> None:
    result, key, step = DetailedTelegramCalendar().process(call.data)
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        pass
    if not result and key:
        msg = bot.edit_message_text(f"Выберите {ru_steps[LSTEP[step]]} {data['move']}",
                                    call.message.chat.id,
                                    call.message.message_id,
                                    reply_markup=key)
        messages.append(msg)
    elif result:
        bot.set_state(call.from_user.id, UserState.calendar_check, call.message.chat.id)
        if data.get('date_in'):
            data['date_out'] = result
        else:
            data['date_in'] = result
        button_ok = InlineKeyboardButton(text='Продолжить', callback_data='ok')
        button_rewrite = InlineKeyboardButton(text='Выбрать заново', callback_data='rewrite')
        keyboard = InlineKeyboardMarkup().add(button_ok, button_rewrite, row_width=2)
        bot.edit_message_text(
            f"Вы выбрали дату {data['move']}: {result}",
            call.message.chat.id,
            call.message.id,
            reply_markup=keyboard
        )


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


@bot.message_handler(state=UserState.calendar_ok)
@recording_msg
def max_price_request(call: CallbackQuery) -> None:
    del_msg()
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        pass
    if data['command'] == 'bestdeal':
        bot.set_state(call.from_user.id, UserState.max_price, call.message.chat.id)
        msg = bot.send_message(call.from_user.id, "Напишите максимальную цену для поиска"
                                                  "\nПример: 250")
        messages.append(msg)
    else:
        bot.set_state(call.from_user.id, UserState.distance, call.message.chat.id)
        quantity_request(call)


@bot.message_handler(state=UserState.max_price)
@recording_msg
def min_price_request(message: Message) -> None:
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
                                                         '\nЧто то не так, давайте попробуем еще раз'
                                                         '\nИзбегайте любых символов кроме цифр'
                                                         '\nПример: 75')
            messages.append(msg)


@bot.message_handler(state=UserState.min_price)
@recording_msg
def check_min_price(message: Message) -> None:
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
                                                         '\nЧто то не так, давайте попробуем еще раз'
                                                         '\nИзбегайте любых символов кроме цифр'
                                                         '\nПример: 75')
            messages.append(msg)


@bot.message_handler(state=UserState.check_price)
@recording_msg
def distance_request(message: Message) -> None:
    del_msg()
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.isdigit():
            data['distance'] = int(message.text)
            bot.set_state(message.from_user.id, UserState.distance, message.chat.id)
            quantity_request(message)
        else:
            msg = bot.send_message(message.from_user.id, 'Упс..'
                                                         '\nЧто то не так, давайте попробуем еще раз'
                                                         '\nИзбегайте любых символов кроме цифр'
                                                         '\nПример: 75')
            messages.append(msg)


@bot.message_handler(state=UserState.distance)
@recording_msg
def quantity_request(message: Message | CallbackQuery) -> None:
    if isinstance(message, CallbackQuery):
        chat_id = message.message.chat.id
    else:
        chat_id = message.chat.id
    del_msg()
    bot.set_state(message.from_user.id, UserState.quantity, chat_id)
    msg = bot.send_message(
        message.from_user.id,
        text="Сколько отелей показать?",
        reply_markup=markup()
    )
    messages.append(msg)


@bot.callback_query_handler(state=UserState.quantity, func=lambda call: call.data)
@recording_msg
def show_photo(call: CallbackQuery) -> None:
    del_msg()
    bot.set_state(call.from_user.id, UserState.show_photo, call.message.chat.id)
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['quantity'] = int(call.data)

    msg = bot.send_message(
        call.from_user.id,
        text="Сколько фото показать по каждому отелю?",
        reply_markup=markup(photo=True)
    )
    messages.append(msg)


@bot.callback_query_handler(state=UserState.show_photo, func=lambda call: call.data)
@recording_msg
def reply(call: CallbackQuery) -> None:
    del_msg()
    bot.set_state(call.from_user.id, UserState.switch, call.message.chat.id)
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['show_photo'] = int(call.data)
    msg = bot.send_message(call.message.chat.id, 'Минуточку...')
    messages.append(msg)
    price_in = prices.get(data['command'], data.get('prices'))
    get_result = process(data, price_in)

    switch(call.message, get_result)
