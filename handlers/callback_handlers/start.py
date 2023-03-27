from telebot.types import CallbackQuery

from handlers.message_handlers.start import start
from loader import bot
from states.state_info import UserState


@bot.callback_query_handler(state=UserState.switch, func=lambda call: call.data == 'start')
def callback_start(call: CallbackQuery) -> None:
    start(call)
