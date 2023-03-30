from telebot.types import CallbackQuery

from database.models import User, UserRequest


def search_history(call: CallbackQuery) -> list:
    """
    Gets max 10 last queries from user from database.
    :param call:
    :return: list of requests
    """
    user = User.get(user_id=call.from_user.id)
    db_request = (
        UserRequest
        .select()
        .limit(10)
        .where(UserRequest.user_id == user.user_id)
        .order_by(UserRequest.date.desc())
    )
    return [
        response
        for response
        in db_request
    ]
