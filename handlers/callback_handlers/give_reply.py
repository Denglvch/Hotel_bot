from telebot.types import CallbackQuery

from api.api_process import process
from handlers.util_data import prices
from loader import bot
from messages_recording.action import recording_msg, del_msg, bot_send_message
from pagination.switch import page_switcher
from states.state_info import UserState


@bot.callback_query_handler(state=UserState.show_photo, func=lambda call: call.data)
@recording_msg
def reply(call: CallbackQuery) -> None:
    """
    The function writes the necessary user data,
    receives a response from the api based on it,
    and sends it to the pagination function.
    :param call:
    :return: None
    """
    del_msg(call.message.chat.id)
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

    bot_send_message(call.message.chat.id, 'Минуточку...')
    data['message_list'] = process(user_data=data)

    if isinstance(data['message_list'], str):
        print(data['message_list'])
    else:
        page_switcher(call)
