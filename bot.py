import telebot
import os
from dotenv import load_dotenv
load_dotenv()

#get the API_KEY and CHAT_ID from .env file

BOT_API_KEY = os.getenv('BOT_API_KEY')
MY_CHAT_ID = int(os.getenv('MY_CHAT_ID'))

bot = telebot.TeleBot(BOT_API_KEY)
