import logging
import sys


def get_logger(name, level=logging.INFO):
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        handler = logging.StreamHandler(sys.stderr)
        logger.addHandler(handler)

    return logger
