import os
from dotenv import load_dotenv
load_dotenv()

bot_token = os.environ.get('BOT_TOKEN')
images_path = os.environ.get('IMAGES_PATH')

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'JPG']
OTHER_IMAGE_EXTENSIONS = ['png', 'gif']

class Config:
    def __init__(self, name: str):
        self.name = name
        
webhook = Config('webhook')
webhook.use_webhook = os.environ.get('USE_WEBHOOK') == 'True'
webhook.host = os.environ.get('WEBHOOK_URL')
webhook.port = os.environ.get('WEBHOOK_PORT')
webhook.listen = '0.0.0.0'
webhook.cert = os.environ.get('WEBHOOK_CERT')
webhook.priv = os.environ.get('WEBHOOK_PRIV')