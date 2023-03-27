from telebot.types import Message, CallbackQuery

from handlers.markups import markup
from loader import bot
from messages_recording.action import recording_msg, del_msg, bot_send_message
from states.state_info import UserState


@bot.message_handler(state=UserState.distance)
@recording_msg
def quantity_request(message: Message | CallbackQuery) -> None:
    if isinstance(message, CallbackQuery):
        chat_id = message.message.chat.id
    else:
        chat_id = message.chat.id
    del_msg(chat_id)
    bot.set_state(message.from_user.id, UserState.quantity, chat_id)
    bot_send_message(
        message.from_user.id,
        text="Сколько отелей показать?",
        reply_markup=markup()
    )
