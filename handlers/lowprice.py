import datetime
import json
from datetime import date

from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from api.api_process import process
from api.get.collection import create_collection
from database.db_read import search_history
from database.db_write import db_add_user
from loader import bot
from messages_recording.action import recording_msg, del_msg, messages
from pagination.switch import page_switcher
from states.state_info import UserState

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

text_command = {
    'lowprice': 'Самые низкие цены',
    'highprice': 'Самые высокие цены',
    'bestdeal': 'Лучшие цены по расположению'
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


@bot.callback_query_handler(state=UserState.start, func=lambda call: call.data == 'history')
@recording_msg
def history_check(call: CallbackQuery):
    db_response = search_history(call)
    if db_response:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['command'] = call.data # костыль починить в дб райт
            data['history'] = {str(num): json.loads(old.request) for num, old in enumerate(db_response, 1)}  # optimized need
        buttons = [
            InlineKeyboardButton(text=resp.text, callback_data=str(num))
            for num, resp
            in enumerate(db_response, 1)
        ]
        keyboard = InlineKeyboardMarkup().add(*buttons, row_width=1)
        bot.set_state(call.from_user.id, UserState.history_look, call.message.chat.id)
        msg = bot.send_message(call.message.chat.id, text='Выберите запрос для просмотра', reply_markup=keyboard)
        messages.append(msg)

    else:
        msg = bot.send_message(call.message.chat.id, 'В истории пока ничего нет.\nПопробуйте сделать первый запрос)')
        messages.append(msg)
        start(call)


@bot.callback_query_handler(state=UserState.history_look, func=lambda call: call.data)
@recording_msg
def history_look(call: CallbackQuery):
    del_msg()
    bot.set_state(call.from_user.id, UserState.switch, call.message.chat.id)
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        pass
    text, photo_links = data['history'][call.data]['response'][0] # убрать лишние скобеи при записи в дбрайт
    print(photo_links)
    text, mediagroup = [
        result
        for result
        in create_collection(data, text=text, photo_links=photo_links)
    ]
    msg = bot.send_message(call.message.chat.id, 'Минуточку...')
    messages.append(msg)

    media_group = bot.send_media_group(call.message.chat.id, mediagroup)
    bot.send_message(
        call.message.chat.id,
        text=text,
    )



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
    history = InlineKeyboardButton(text='История поиска', callback_data='history')
    test_1 = InlineKeyboardButton(text='Test1', callback_data='test1')
    test_2 = InlineKeyboardButton(text='Test2', callback_data='test2')
    buttons = InlineKeyboardMarkup().add(lowprice, highprice, bestdeal, history, test_1, test_2, row_width=1)
    msg = bot.send_message(chat_id, text='Что будем смотреть?', reply_markup=buttons)
    bot.set_state(message.from_user.id, UserState.start, chat_id)
    # bot.set_state(message.from_user.id, UserState.test, chat_id)
    messages.append(msg)


@bot.callback_query_handler(state=UserState.test, func=lambda call: call.data)
@recording_msg
def test(call: CallbackQuery):
    del_msg()
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        pass
    bot.set_state(call.from_user.id, UserState.switch, call.message.chat.id)
    if call.data == 'test1':
        data.update({'user_id': 47653108, 'command': 'lowprice', 'text_command': 'Самые низкие цены', 'city': 'milan',
                     'move': 'выезда', 'date_in': datetime.date(2023, 8, 15), 'date_out': datetime.date(2023, 8, 23),
                     'quantity': 4, 'show_photo': 4, 'price_in': None,
                     'text_response': 'Самые низкие цены для milan, отелей: 4, 4 фото', 'response': [
                ['\nОтель: Rosa Grand Milano\nЦена за ночь: $288\nЦена за 8 ночей: 2304\nРасстояние до центра: 0.41 км',
                 [
                     'https://images.trvl-media.com/lodging/1000000/10000/2900/2875/e4ba20a7.jpg?impolicy=resizecrop&rw=500&ra=fit',
                     'https://images.trvl-media.com/lodging/1000000/10000/2900/2875/8796117a.jpg?impolicy=resizecrop&rw=500&ra=fit',
                     'https://images.trvl-media.com/lodging/1000000/10000/2900/2875/a27dd8c7.jpg?impolicy=resizecrop&rw=500&ra=fit',
                     'https://images.trvl-media.com/lodging/1000000/10000/2900/2875/03b9382d.jpg?impolicy=resizecrop&rw=500&ra=fit']]]})

        msg = bot.send_message(call.message.chat.id, 'Минуточку...')
        data['message_list'] = process(data)
        messages.append(msg)
        page_switcher(call)
    elif call.data == 'test2':
        data.update(
            {'user_id': 47653108, 'command': 'lowprice', 'text_command': 'Самые низкие цены', 'city': 'new york',
             'move': 'выезда', 'date_in': datetime.date(2023, 5, 17), 'date_out': datetime.date(2023, 5, 24),
             'quantity': 3, 'show_photo': 3, 'price_in': None,
             'text_response': 'Самые низкие цены для new york, отелей: 4, 4 фото', 'response': [[
                                                                                                    '\nОтель: Super 8 by Wyndham Jamaica North Conduit\nЦена за ночь: $126\nЦена за 7 ночей: 882\nРасстояние до центра: 12.08 км',
                                                                                                    [
                                                                                                        'https://images.trvl-media.com/lodging/7000000/6040000/6036600/6036585/bb65528c.jpg?impolicy=resizecrop&rw=500&ra=fit',
                                                                                                        'https://images.trvl-media.com/lodging/7000000/6040000/6036600/6036585/128cdf7a.jpg?impolicy=resizecrop&rw=500&ra=fit',
                                                                                                        'https://images.trvl-media.com/lodging/7000000/6040000/6036600/6036585/f7a48a0c.jpg?impolicy=resizecrop&rw=500&ra=fit',
                                                                                                        'https://images.trvl-media.com/lodging/7000000/6040000/6036600/6036585/e24c7506.jpg?impolicy=resizecrop&rw=500&ra=fit']]]})
        # data['show_photo'] = 0
        msg = bot.send_message(call.message.chat.id, 'Минуточку...')
        data['message_list'] = process(data)
        messages.append(msg)
        page_switcher(call)
    else:
        bot.set_state(call.from_user.id, UserState.start, call.message.chat.id)
        city_request(call)


@bot.callback_query_handler(state=UserState.start, func=lambda call: call.data != 'history')
@recording_msg
def city_request(call: CallbackQuery) -> None:
    del_msg()

    bot.set_state(call.from_user.id, UserState.city, call.message.chat.id)
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['user_id'] = call.from_user.id
        data['command'] = call.data
        data['text_command'] = text_command[call.data]
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
        data['price_in'] = prices.get(data['command'], data.get('prices'))
        data['text_response'] = (
            f'{data.get("text_command")} '
            f'для {data.get("city")}, '
            f'отелей: {data.get("quantity")}, '
            f'{data.get("show_photo") or "без"} фото'
        )
    msg = bot.send_message(call.message.chat.id, 'Минуточку...')
    messages.append(msg)
    # get_result = process(data)
    data['message_list'] = process(data)
    # print(data)

    page_switcher(call)


@bot.callback_query_handler(state=UserState.switch, func=lambda call: call.data != 'start')
def _page_callback(call: CallbackQuery) -> None:
    if not call.data == 'start':
        page = int(call.data.split('#')[1])
        del_msg()
        page_switcher(call, page)
