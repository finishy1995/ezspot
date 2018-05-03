import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.DEBUG)
formatter_debug = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
formatter_info = logging.Formatter('%(levelname)s : %(message)s')
formatter_warning = logging.Formatter('%(levelname)s : %(message)s')
formatter_error = logging.Formatter('%(message)s')

file_fold = os.path.expanduser('~/.ezspot')
file_path = os.path.expanduser('~/.ezspot/log')
if not os.path.exists(file_fold):
    os.makedirs(file_fold)
if not os.path.isfile(file_path):
    file = open(file_path, 'w')
    file.close()
file_handler = logging.FileHandler(file_path)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter_debug)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter_info)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.debug('')

def setLevel(level):
    if level == 'DEBUG':
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter_debug)
    elif level == 'INFO':
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter_info)
    elif level == 'WARNING':
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(formatter_warning)
    elif level == 'ERROR':
        console_handler.setLevel(logging.ERROR)
        console_handler.setFormatter(formatter_error)

def info(message, **kwargs):
    logger.info(message, **kwargs)
    
def debug(message,**kwargs):
    logger.debug(message, **kwargs)
    
def warning(message, **kwargs):
    logger.warning(message, **kwargs)

def error(message, **kwargs):
    logger.error(message, **kwargs)

def error_traceback(message):
    error(message, exc_info = True)
