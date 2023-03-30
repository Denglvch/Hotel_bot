from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from handlers.util_data import ru_steps
from loader import bot
from states.state_info import UserState


@bot.callback_query_handler(state=UserState.calendar_start, func=DetailedTelegramCalendar.func())
def calendar_steps(call: CallbackQuery) -> None:
    """
    The function controls the switching of the calendar display mode to select the year, month, day,
    and also writes the necessary user data.
    :param call:
    :return: None
    """
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
