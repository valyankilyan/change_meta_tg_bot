import os
from dotenv import load_dotenv
load_dotenv()

bot_token = os.environ.get('BOT_TOKEN')
images_path = os.environ.get('IMAGES_PATH')

BEST_EXTENSIONS = ['jpg', 'jpeg', 'jpe', 'jif', 'jfif', 'jfi']
OTHER_ALLOWED_EXTENSIONS = ['png',
                            'heif', 'heic', 'avif']
NOT_ALLOWED_IMAGE_EXTENSIONS = ['gif',
                                'webp',
                                'tiff', 'tif',
                                'psd',
                                'raw', 'arw', 'cr2', 'nrw', 'k25',
                                'bmp', 'dib',
                                'indd', 'ind', 'indt',
                                'jp2', 'j2k', 'jpf', 'jpx', 'jpm', 'mj2',
                                'svg', 'svgz',
                                'ai', 'eps', 'pdf']

class Config:
    def __init__(self, name: str):
        self.name = name
        
webhook = Config('webhook')
webhook.use_webhook = os.environ.get('USE_WEBHOOK') == 'True'
webhook.host = os.environ.get('WEBHOOK_URL')
webhook.port = os.environ.get('WEBHOOK_PORT')
webhook.listen = '127.0.0.1'
webhook.cert = os.environ.get('WEBHOOK_CERT')
webhook.priv = os.environ.get('WEBHOOK_PRIV')