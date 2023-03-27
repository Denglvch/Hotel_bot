from datetime import date

from telebot.types import Message, CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

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
