from telebot.types import CallbackQuery

from loader import bot
from messages_recording.action import del_msg
from pagination.switch import page_switcher
from states.state_info import UserState


@bot.callback_query_handler(state=UserState.switch, func=lambda call: call.data != 'start')
def page_callback(call: CallbackQuery) -> None:
    if not call.data == 'start':
        page = int(call.data.split('#')[1])
        del_msg(call.message.chat.id)
        page_switcher(call, page)
