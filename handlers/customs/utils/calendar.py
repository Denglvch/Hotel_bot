from datetime import date

from telebot.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from handlers.customs.prices import max_price_request
from handlers.util_data import ru_steps
from loader import bot
from messages_recording.action import recording_msg, del_msg, bot_send_message
from states.state_info import UserState


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
    del_msg(chat_id)
    bot.set_state(message.from_user.id, UserState.calendar_start, chat_id)
    calendar_obj = DetailedTelegramCalendar(min_date=date.today())
    calendar, step = calendar_obj.build()
    bot_send_message(
        chat_id,
        f"Выберите {ru_steps[LSTEP[step]]} {data['move']}",
        reply_markup=calendar
    )


@bot.callback_query_handler(state=UserState.calendar_start, func=DetailedTelegramCalendar.func())
def calendar_steps(call: CallbackQuery) -> None:
    result, key, step = DetailedTelegramCalendar().process(call.data)
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        pass
    if not result and key:
        bot.edit_message_text(f"Выберите {ru_steps[LSTEP[step]]} {data['move']}",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
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
