from telebot.types import CallbackQuery

from handlers.markups import markup
from loader import bot
from messages_recording.action import recording_msg, del_msg, bot_send_message
from states.state_info import UserState


@bot.callback_query_handler(state=UserState.quantity, func=lambda call: call.data)
@recording_msg
def show_photo(call: CallbackQuery) -> None:
    """
    The function prompts the user to select the desired number of photos to display for each hotel or refuse it.
    :param call:
    :return: None
    """
    del_msg(call.message.chat.id)
    bot.set_state(call.from_user.id, UserState.show_photo, call.message.chat.id)
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['quantity'] = int(call.data)

    bot_send_message(
        call.from_user.id,
        text="Сколько фото показать по каждому отелю?",
        reply_markup=markup(photo=True)
    )
