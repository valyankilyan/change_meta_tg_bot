from loggingconfig import getLogger
log = getLogger(__name__)

from exif import Image
from config import bot_token, images_path, ALLOWED_EXTENSIONS
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
    path = downloadPhoto(message.photo[2].file_id, 'photo')
    sendChangedPhoto(message, path)

@bot.message_handler(content_types=['document'])
def documentHandler(message):
    log.debug(message)
    if message.document.file_name.split('.')[-1] in ALLOWED_EXTENSIONS:
        path = downloadPhoto(message.document.file_id, 'document', message.document.file_name)        
        sendChangedPhoto(message, path)
    else:
        bot.send_message(message.chat.id, 'Вы кажется, не фотографию отправили')
        
def sendChangedPhoto(message, path):
    cords = getUserByTg(message.from_user.id).cords
    changeExif(path, cords)
    with open(path, 'rb') as photo:
        bot.send_document(message.chat.id, photo)
    
def downloadPhoto(file_id, type, file_name=None):
    if type == 'photo':
        path = f'{images_path}/{file_id}.jpg'
    if type == 'document':
        path = f'{images_path}/{file_name}'
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(path, 'wb') as new_file:
        new_file.write(downloaded_file)
    return path

def changeExif(path, cords):
    with open(path, 'rb') as file:
        image = Image(file)
        log.debug('----------------------')
        log.debug(f'file {path} has read')
        try:
            log.debug(f"Latitude: {image.gps_latitude} {image.gps_latitude_ref}")
            log.debug(f"Longitude: {image.gps_longitude} {image.gps_longitude_ref}")
        except:
            log.debug(f'Image {path} does not have gps exif data')
    image.gps_latitude = cords.latitude
    image.gps_latitude_ref = cords.latitude_ref
    image.gps_longitude = cords.longitude
    image.gps_longitude_ref = cords.longitude_ref
    with open(f'{path}', 'wb') as updated_file:
        updated_file.write(image.get_file())

@bot.message_handler(func=lambda message: True)
def errorHandler(message):
    bot.reply_to(message, "Извини, кажется, я не расчитан на такое.")

bot.polling()