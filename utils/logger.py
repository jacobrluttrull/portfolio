import logging
import logging.handlers
import sys

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        file_handler = logging.handlers.RotatingFileHandler('app.log', maxBytes=5*1024*1024, backupCount=3)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        logger.addHandler(stdout_handler)

    return logger
