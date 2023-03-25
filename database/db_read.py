from telebot.types import CallbackQuery

from database.models import User, UserRequest, UserMessage


def search_history(call: CallbackQuery) -> list:
    user = User.get(user_id=call.from_user.id)
    db_request = (
        UserRequest
            .select()
            .limit(10)
            .where(UserRequest.user_id == user.user_id).order_by(UserRequest.date.desc())
    )
    return [
        response
        for response
        in db_request
    ]


def messages_from_user(chat_id: int) -> list:
    messages = (
        UserMessage
            .select()
            .where(UserMessage.chat_id == chat_id)
    )
    UserMessage.delete().where(UserMessage.chat_id in messages)
    return [
        msg
        for msg
        in messages
    ]
