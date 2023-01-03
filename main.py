from loader import bot
from telebot import custom_filters
import commands


if __name__ == "__main__":
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    commands.get(bot)
    bot.infinity_polling()
