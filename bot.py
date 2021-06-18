from loggingconfig import getLogger
log = getLogger(__name__)
from config import bot_token

import telebot
bot = telebot.TeleBot(bot_token, parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Привет, я помогу тебе изменить gps данные фотографии. Для начала тебе нужно скинуть мне необходимые координаты.")
 
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    log.info(f'message {message} recieved')
    if message.location:
        log.info(f'data = {message.location.latitude}, {message.location.longitude}')
        bot.send_message(message.chat.id, f'{message.location.latitude}, {message.location.longitude}')
	
@bot.message_handler(content_types=['location'])
def handle_location(message):
    log.info(f'data = {message.location.latitude}, {message.location.longitude}')
    bot.send_message(message.chat.id, f'{message.location.latitude}, {message.location.longitude}')

bot.polling()