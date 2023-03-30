from telebot.types import CallbackQuery

from api.get.collection import create_collection
from loader import bot
from messages_recording.action import recording_msg, del_msg
from pagination.switch import page_switcher
from states.state_info import UserState


@bot.callback_query_handler(state=UserState.history_look, func=lambda call: call.data)
@recording_msg
def history_look(call: CallbackQuery) -> None:
    """
    The function sends the content of the selected request from the request history to the user.
    :param call:
    :return: None
    """
    del_msg(call.message.chat.id)
    bot.set_state(call.from_user.id, UserState.switch, call.message.chat.id)
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        pass
    response_from_db = data['history'][call.data]['response']
    if all(isinstance(elem, list) for elem in response_from_db):
        message_list = [
            create_collection(user_data=data, text=text, photo_links=photo_links)
            for text, photo_links
            in response_from_db
        ]
    else:
        message_list = [
            create_collection(user_data=data, text=text)
            for text
            in response_from_db
        ]
    data['message_list'] = message_list
    page_switcher(call)
