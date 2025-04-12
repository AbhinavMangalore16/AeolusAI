import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name=__name__):
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers
    if not logger.handlers:
        handler = RotatingFileHandler("logs/weather.log", maxBytes=500000, backupCount=3)
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s — %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger