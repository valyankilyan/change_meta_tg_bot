from loggingconfig import getLogger
log = getLogger(__name__)

from exif import Image
from config import bot_token
from models import User, getUserByTg
import telebot
bot = telebot.TeleBot(bot_token, parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def sendWelcome(message):
    if getUserByTg(message.from_user.id) == None:
        User(
            message.from_user.id,
            message.from_user.username,
            message.chat.id
        ).commit()
    bot.reply_to(message, "Привет, я помогу тебе изменить gps данные фотографии. \
Для начала тебе нужно скинуть мне необходимые координаты.")

@bot.message_handler(content_types=['location'])
def locationHandler(message):
    log.info(f'data = {message.location.latitude}, {message.location.longitude}')
    user = getUserByTg(message.from_user.id)
    user.setCords(message.location.latitude, message.location.longitude)
    bot.send_message(message.chat.id, f'Кординаты обновлены: {message.location.latitude}, {message.location.longitude}')

@bot.message_handler(commands=['getCurrentCords'])
def sendCurrentCords(message):
    user = getUserByTg(message.from_user.id)
    cords = user.cords
    if cords:
        latitude, longitude = cords.getTelegramTypeCords()
        bot.send_location(message.chat.id, latitude, longitude)
    else:
        bot.send_message(message.chat.id, 'Вы ещё ни разу не отправляли мне местоположение.')
    
# @bot.message_handler(func=lambda message: True, content_types=['photo', 'document'])
# def default_command(message):
#     bot.send_message(message.chat.id, "This is the default command handler.")
    
@bot.message_handler(content_types=['photo'])
def photoHandler(message):
    log.debug(message)
    bot.send_message(message.chat.id, 'фото получено')

@bot.message_handler(content_types=['document'])
def documentHandler(message):
    log.debug(message)
    bot.send_message(message.chat.id, 'документ получаен')


@bot.message_handler(func=lambda message: True)
def errorHandler(message):
    bot.reply_to(message, "Извини, кажется, я не расчитан на такое.")

bot.polling()