import queue
import logging
from logging.handlers import QueueHandler, QueueListener

log_queue = queue.Queue()
queue_handler = QueueHandler(log_queue)

listener = QueueListener(log_queue, logging.StreamHandler(), logging.FileHandler('log.txt'))

logger = logging.getLogger()
logger.addHandler(queue_handler)
logger.setLevel(logging.INFO)