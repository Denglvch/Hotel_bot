from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def markup(photo: bool = False) -> InlineKeyboardMarkup:
    keyboard = [
        InlineKeyboardButton(text=num, callback_data=num)
        for num
        in range(3, 11)
    ]
    buttons = InlineKeyboardMarkup().add(*keyboard, row_width=8)
    if photo:
        no_photo = InlineKeyboardButton(text='Без фото', callback_data='0')
        buttons.add(no_photo)

    return buttons
