import logging
import os
from datetime import datetime


class Logger:
    def __init__(self):
        self.logger = logging.getLogger('image crawler')
        self.logger.setLevel(logging.DEBUG)

        self.base_dir = 'log/app'
        os.makedirs(self.base_dir, exist_ok=True)

        self.configure_default_logger()
        self.configure_error_logger()

    def configure_error_logger(self):
        formatter_error = logging.Formatter("%(asctime)s %(levelname)s\n%(message)s")
        handler_error = logging.FileHandler(f'{self.base_dir}/{datetime.now().strftime("%Y%m%d")}.error.log')
        handler_error.setLevel(logging.ERROR)
        handler_error.setFormatter(formatter_error)

        self.logger.addHandler(handler_error)

    def configure_default_logger(self):
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        handler_stream = logging.StreamHandler()
        handler = logging.FileHandler(f'{self.base_dir}/{datetime.now().strftime("%Y%m%d")}.log')
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)
        self.logger.addHandler(handler_stream)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
