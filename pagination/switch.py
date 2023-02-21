
from telebot import TeleBot
from telebot.types import Message
from telegram_bot_pagination import InlineKeyboardPaginator, InlineKeyboardButton

from messages_recording.action import del_msg, messages


def go(msg):
    def start(func):
        func(msg)
    return start


def switch(bot: TeleBot, message: Message, data: list):

    @bot.callback_query_handler(func=lambda call: call.data)
    def characters_page_callback(call):
        page = int(call.data.split('#')[1])
        del_msg()
        send_page(call.message, page)

    def send_page(message, page=1):
        messages.append(message)
        paginator = InlineKeyboardPaginator(
            len(data),
            current_page=page,
            data_pattern='character#{page}'
        )

        paginator.add_after(InlineKeyboardButton('Меню бота', callback_data='start'))

        result = data[page-1]
        if isinstance(result, str):
            msg = bot.send_message(
                message.chat.id,
                result,
                reply_markup=paginator.markup,
                parse_mode='Markdown'
            )
            messages.append(msg)
        else:
            text, photo = result[0], result[1]
            media_group = bot.send_media_group(message.chat.id, photo)
            for msg_from in media_group:
                messages.append(msg_from)

            keyboard = bot.send_message(
                message.chat.id,
                text=text,
                reply_markup=paginator.markup,
                parse_mode='Markdown'
            )
            messages.append(keyboard)


    @go(message)
    def go_switch(message):
        # bot.set_state(message.from_user.id, UserState.switch, message.chat.id)
        send_page(message)
