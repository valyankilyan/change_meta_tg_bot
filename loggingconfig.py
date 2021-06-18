import logging 
import logging.config

logging.config.fileConfig('.conf/logging.conf')
log = logging.getLogger(__name__)
log.info('Logging started')

def getLogger(name):
    return logging.getLogger(name)
