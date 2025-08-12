import logging
from pythonjsonlogger import jsonlogger
import sys

def log_configuring():

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    handler = logging.StreamHandler(sys.stdout)
    format = "%(asctime)s %(name)s %(levelname)s %(message)s"
    formatter = jsonlogger.JsonFormatter(format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

