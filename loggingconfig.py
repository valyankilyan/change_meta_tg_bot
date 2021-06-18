import logging 
import logging.config

def getLogger(name):
    logging.config.fileConfig('.conf/logging.conf')
    logger = logging.getLogger(name)
    return logger
    

# for l in logging.root.manager.loggerDict:
#     logging.getLogger(l).disabled = False
