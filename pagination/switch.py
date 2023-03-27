from telebot.types import CallbackQuery
from telegram_bot_pagination import InlineKeyboardPaginator, InlineKeyboardButton

from database.db_write import db_add_message
from loader import bot


def page_switcher(call: CallbackQuery, page: int = 1,  disable_notification=True) -> None:
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        message_list = data['message_list']
    db_add_message(call)
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
            parse_mode='Markdown',
            disable_notification=disable_notification
        )
        db_add_message(msg)
    else:
        text, photo = result[0], result[1]
        media_group = bot.send_media_group(
            call.message.chat.id,
            photo,
            disable_notification=disable_notification
        )
        for msg_from in media_group:
            db_add_message(msg_from)

        keyboard = bot.send_message(
            call.message.chat.id,
            text=text,
            reply_markup=paginator.markup,
            parse_mode='Markdown',
            disable_notification=disable_notification
        )
        db_add_message(keyboard)
