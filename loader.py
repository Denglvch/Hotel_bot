import telebot
from telebot import custom_filters
from telebot.storage import StateMemoryStorage
from config import config


storage = StateMemoryStorage()
bot = telebot.TeleBot(config.get('token'), state_storage=storage)
bot.add_custom_filter(custom_filters.StateFilter(bot))
