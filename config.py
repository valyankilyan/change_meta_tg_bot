import os
from dotenv import load_dotenv
load_dotenv()

bot_token = os.environ.get('BOT_TOKEN')
images_path = os.environ.get('IMAGES_PATH')
src_image_path = os.environ.get('SRC_IMAGE_PATH')

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'JPG']
