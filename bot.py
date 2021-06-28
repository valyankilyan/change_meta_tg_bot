from loggingconfig import getLogger
log = getLogger(__name__)

import flask
import telebot
import time
from config import NOT_ALLOWED_IMAGE_EXTENSIONS, bot_token, images_path, BEST_EXTENSIONS, OTHER_ALLOWED_EXTENSIONS, webhook
from models import User, getUserByTg, getAllUsers, getUser
from changer import changeGPS, changeFormat, getTrueFormat, replace_last,\
replaceWithTrueFormat, deletePhoto
import bot_answers

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

@app.route('/test')
def test_page():
    return 'it works well'

@bot.message_handler(commands=['start', 'help'])
def sendWelcome(message):
    if getUserByTg(message.from_user.id) == None:
        User(
            message.from_user.id,
            message.from_user.username,
            message.chat.id
        ).commit()
        try:
            admin = [getUser(1), getUser(2)]
            for a in admin:
                bot.send_message(a.chat_id, f'newUser {message.from_user.username}')
        except:
            log.info(f'I suppose u did not register')
    bot.send_message(message.chat.id, bot_answers.help)

@bot.message_handler(content_types=['location'])
def locationHandler(message):
    log.info(f'data = {message.location.latitude}, {message.location.longitude}')
    user = getUserByTg(message.from_user.id)
    user.setCords(message.location.latitude, message.location.longitude)
    bot.send_message(message.chat.id, bot_answers.cords_was_updated)

@bot.message_handler(commands=['getcurrentcords'])
def sendCurrentCords(message):
    user = getUserByTg(message.from_user.id)
    cords = user.cords
    if cords:
        latitude, longitude = cords.getTelegramTypeCords()
        bot.send_location(message.chat.id, latitude, longitude)
        bot.send_message(message.chat.id, bot_answers.send_current_cords)
    else:
        bot.send_message(message.chat.id, bot_answers.first_send_location)
    
# @bot.message_handler(func=lambda message: True, content_types=['photo', 'document'])
# def default_command(message):
#     bot.send_message(message.chat.id, "This is the default command handler.")
    
@bot.message_handler(content_types=['photo'])
def photoHandler(message):
    log.debug(f'user {message.from_user.username} sent us photo')
    if getUserByTg(message.from_user.id).cords:
        path = downloadPhoto(message.photo[2].file_id, 'photo')
        sendChangedPhoto(message, path)
    else:
        bot.send_message(message.chat.id, bot_answers.first_send_location)

@bot.message_handler(content_types=['document'])
def documentHandler(message):
    log.debug(f'user {message.from_user.username} sent us document {message.document.file_name}')
    if getUserByTg(message.from_user.id).cords:
        fmt = message.document.file_name.split('.')[-1]
        filename = replace_last(message.document.file_name, fmt, fmt.lower())
        path = downloadPhoto(message.document.file_id, 'document', filename) 
        true_fmt = getTrueFormat(path)
        fmt = fmt.lower()
        log.debug(f'Format is {fmt}, true format is {true_fmt}')
        if true_fmt != fmt:
            path = replaceWithTrueFormat(path, fmt, true_fmt)
            fmt = true_fmt
            
        if fmt in BEST_EXTENSIONS:            
            sendChangedPhoto(message, path)
        elif fmt in OTHER_ALLOWED_EXTENSIONS:
            log.debug('Image is not JPG, but ill try to deal with it')
            bot.send_message(message.chat.id, bot_answers.handle_not_jpg_image)            
            sendChangedPhoto(message, path, fmt)            
        elif fmt in NOT_ALLOWED_IMAGE_EXTENSIONS:
            log.debug("I don't work with this type of images.")
            bot.send_message(message.chat.id,
                bot_answers.cant_handle_image.format(getAllAllowedExtensions()))
        else:
            deletePhoto(path)
            bot.send_message(message.chat.id, bot_answers.its_not_an_image)
    else:
        bot.send_message(message.chat.id, bot_answers.first_send_location)   

def sendChangedPhoto(message, path, fmt=None):
    user = getUserByTg(message.from_user.id)
    cords = user.cords
    if fmt != None:
        log.debug("I suppose, format isn't jpeg, okay, let's change format")
        path = changeFormat(path, fmt)
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

def getAllAllowedExtensions():
    out = ''
    for e in BEST_EXTENSIONS:
        out+= e + ' '
    for e in OTHER_ALLOWED_EXTENSIONS:
        out+= e + ' '
    return e

@bot.message_handler(commands=['sendUserData'])
def sendUserData(message):
    if getUserByTg(message.from_user.id).id not in [1, 2]:
        errorHandler(message)
    else:
        users = getAllUsers()
        out = ''
        for u in users:
            out+= f'@{u.tg_username} - {u.sent_photos}\n'
        bot.send_message(message.chat.id, out)

@bot.message_handler(content_types=['audio', 'sticker', 'video', 'video_note', 'voice',
                                    'contact', 'pinned_message'])
def iAmNotWorkingWithThat(message):
    bot.send_message(message.chat.id, bot_answers.i_am_not_working_with_that)

@bot.message_handler(func=lambda message: True)
def errorHandler(message):
    bot.reply_to(message, "Извини, кажется, я не расчитан на такое.")

if webhook.use_webhook:
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
    app.run(host=WEBHOOK_LISTEN,
            port=WEBHOOK_PORT,
            debug=False)
    log.info("Bot Worker webhook works")
else:
    bot.polling(none_stop=True)

log.info("Bot worker started")