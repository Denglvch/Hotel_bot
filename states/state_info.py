from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    city = State()
    quantity = State()
    price_min = State()
    price_max = State()


