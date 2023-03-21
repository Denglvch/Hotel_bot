from telebot.types import CallbackQuery
from telegram_bot_pagination import InlineKeyboardPaginator, InlineKeyboardButton

from loader import bot
from messages_recording.action import messages


def page_switcher(call: CallbackQuery, page: int = 1) -> None:
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        message_list = data['message_list']
    messages.append(call)
    paginator = InlineKeyboardPaginator(
        len(message_list),
        current_page=page,
        data_pattern='#{page}'
    )

    paginator.add_after(InlineKeyboardButton('Меню бота', callback_data='start'))

    result = message_list[page - 1]
    if isinstance(result, str):
        msg = bot.send_message(
            call.message.chat.id,
            result,
            reply_markup=paginator.markup,
            parse_mode='Markdown'
        )
        messages.append(msg)
    else:
        text, photo = result[0], result[1]
        media_group = bot.send_media_group(call.message.chat.id, photo)
        for msg_from in media_group:
            messages.append(msg_from)

        keyboard = bot.send_message(
            call.message.chat.id,
            text=text,
            reply_markup=paginator.markup,
            parse_mode='Markdown'
        )
        messages.append(keyboard)
