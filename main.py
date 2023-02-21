from loader import bot
import commands


if __name__ == "__main__":
    commands.get(bot)
    bot.infinity_polling()