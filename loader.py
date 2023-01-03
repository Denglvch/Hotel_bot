import telebot
from telebot.storage import StateMemoryStorage
from config import config


storage = StateMemoryStorage()
bot = telebot.TeleBot(config.get('token'), state_storage=storage)

