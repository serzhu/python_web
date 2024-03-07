import logging
from pathlib import Path


log_format = "[%(levelname)s] %(asctime)s: %(name)s %(module)s %(funcName)s:%(lineno)d - %(message)s"

p = Path(__file__)
Path(p.parent / 'Logs').mkdir(parents=True, exist_ok=True)
filename = p.parent / 'Logs' / 'bot.log'
file_handler = logging.FileHandler(filename)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(log_format))

def get_logger(name, level):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    return logger

logger = get_logger('bot', logging.DEBUG)                          
 