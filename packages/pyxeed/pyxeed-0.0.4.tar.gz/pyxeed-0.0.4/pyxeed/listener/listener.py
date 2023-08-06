import logging

__all__ = ['Listener']


class Listener():
    def __init__(self):
        self.logger = logging.getLogger("Xeed.Listener")

    async def listening(self, callback):
        """
        callback with format {'header': dict; 'data': encoded data}
        :param callback:
        :return:
        """
        pass

