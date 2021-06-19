from loggingconfig import getLogger
log = getLogger(__name__)

import flask
import telebot
import time
from config import bot_token, images_path, ALLOWED_EXTENSIONS, webhook
from models import User, getUserByTg, getAllUsers
from changer import changeGPS, deletePhoto

WEBHOOK_HOST = webhook.host
WEBHOOK_PORT = webhook.port  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = webhook.listen  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = webhook.cert  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = webhook.priv  # Path to the ssl private key

WEBHOOK_URL_BASE = f'https://{WEBHOOK_HOST}'
WEBHOOK_URL_PATH = f'/api/web-hook/'

bot = telebot.TeleBot(bot_token)
bot.remove_webhook()
time.sleep(0.1)
log.debug('remove_webhook')
app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''

# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook_route():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

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
    path = downloadPhoto(message.photo[2].file_id, 'photo')
    sendChangedPhoto(message, path)

@bot.message_handler(content_types=['document'])
def documentHandler(message):    
    if message.document.file_name.split('.')[-1] in ALLOWED_EXTENSIONS:
        path = downloadPhoto(message.document.file_id, 'document', message.document.file_name)        
        sendChangedPhoto(message, path)
    else:
        bot.send_message(message.chat.id, 'Вы кажется, не фотографию отправили')
        
def sendChangedPhoto(message, path):
    user = getUserByTg(message.from_user.id)
    cords = user.cords
    changeGPS(path, cords)
    with open(path, 'rb') as photo:
        bot.send_document(message.chat.id, photo)    
    deletePhoto(path)
    user.sent_photos+= 1
    user.commit()
    
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

@bot.message_handler(commands=['sendUserData'])
def sendUserData(message):
    if getUserByTg(message.from_user.id).id != 1:
        errorHandler(message)
    else:
        users = getAllUsers()
        out = ''
        for u in users:
            out+= f'@{u.tg_username} - {u.sent_photos}\n'
        bot.send_message(message.chat.id, out)

@bot.message_handler(func=lambda message: True)
def errorHandler(message):
    bot.reply_to(message, "Извини, кажется, я не расчитан на такое.")

if webhook.use_webhook:
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
    app.run(host=WEBHOOK_LISTEN,
            port=WEBHOOK_PORT,
            debug=True)
    log.info("Bot Worker webhook works")
else:
    bot.polling(none_stop=True)

log.info("Bot worker started")