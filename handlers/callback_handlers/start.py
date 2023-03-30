from telebot.types import CallbackQuery

from handlers.message_handlers.start import start
from loader import bot
from states.state_info import UserState


@bot.callback_query_handler(state=UserState.switch, func=lambda call: call.data == 'start')
def callback_start(call: CallbackQuery) -> None:
    """
    Helper function, redirects the call to the main function of starting a dialog.
    :param call:
    :return: None
    """
    start(call)
