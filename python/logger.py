import logging
import sys


class Logger:
    """
    Simple singleton class to encapsulate logging to the Flask app object so
    we can have unified logging.
    """
    instance = None

    def __new__(cls, logger=None):
        if not Logger.instance:
            if not logger:
                raise ValueError("No logger specified on creation of Logger\
                 singleton.")
            Logger.instance = logger
            logger.setLevel(logging.INFO)
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            return Logger.instance
        return Logger.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)
