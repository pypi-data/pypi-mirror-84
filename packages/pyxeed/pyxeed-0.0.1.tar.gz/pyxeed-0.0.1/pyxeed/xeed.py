import logging

from pyxeed.utils.core import LOGGING_LEVEL

__all__ = ['Xeed']


class Xeed():
    def __init__(self):
        self.logger = logging.getLogger("Xeed")
        self.logger.setLevel(LOGGING_LEVEL)