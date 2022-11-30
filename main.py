import telebot

token = '5904422047:AAEQ3Jt8xSMBFM1SSeIFIE7dWtEAzWmH4rM'

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет")


bot.infinity_polling()
