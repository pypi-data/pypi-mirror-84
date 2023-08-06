import datetime
import logging
import os
from logging.handlers import TimedRotatingFileHandler


def configure_rotating_logger(logger_name, debug=False, backup_count=14, hour=3, interval=1):
    """
    Initialize rotate logger

    :param logger_name: name of logger, so you can access it from anywhere with specific logger name
    :param debug: debug used for debugging purpose, if you want write logger.info on file, you can enable debug
    :param backup_count: how many backup count that you want
    :param hour: hour when log change to next file rotate
    :param interval: interval day you want to backup, default each 1 day
    :return:
    """
    logger = logging.getLogger(logger_name)
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    formatter = logging.Formatter(
        "[%(asctime)s.%(msecs)03d] %(levelname)s [%(thread)d] - %(message)s", "%Y-%m-%d %H:%M:%S")
    try:
        os.makedirs('log', exist_ok=True)
        path = f"log/{logger_name}.log"
    except Exception as e:
        path = f'{logger_name}.log'
    time_rotate = datetime.time(hour=hour, minute=0, second=0)
    handler = TimedRotatingFileHandler(path, when='midnight', interval=interval, atTime=time_rotate,
                                       backupCount=backup_count)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
