from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    start = State()
    calendar_start = State()
    calendar_steps = State()
    calendar_check = State()
    calendar_ok = State()
    city = State()
    quantity = State()
    distance = State()
    show_photo = State()
    check_price = State()
    min_price = State()
    max_price = State()
    switch = State()
    history_check = State()
    history_look = State()
    test = State()


