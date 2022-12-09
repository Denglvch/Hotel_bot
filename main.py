import telebot
import commands
from dotenv import dotenv_values

config = dotenv_values('.venv.templates')

bot = telebot.TeleBot(config.get('token'))


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет")


@bot.message_handler(commands=['lowprice'])
def city_request(message):
    city_name = bot.send_message(message.chat.id, "Введите название города")
    bot.register_next_step_handler(city_name, quantity_request)


def quantity_request(message):
    amount_hotels = bot.send_message(message.chat.id, "Сколько отелей показать?")
    bot.register_next_step_handler(amount_hotels, reply, message.text)


def reply(message, city_name):
    bot.send_message(message.chat.id, 'Минуточку...')
    bot.send_message(message.chat.id, commands.lowprice(message.text, city_name))


if __name__ == "__main__":
    bot.infinity_polling()
