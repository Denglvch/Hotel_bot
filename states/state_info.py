from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):

    city = State()
    quantity = State()
    distance = State()
    show_photo = State()
    check_price = State()
    min_price = State()
    max_price = State()
    switch = State()


