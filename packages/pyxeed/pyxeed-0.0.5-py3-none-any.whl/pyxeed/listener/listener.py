import logging

__all__ = ['Listener']


class Listener():
    def __init__(self):
        self.logger = logging.getLogger("Xeed.Listener")
        formatter = logging.Formatter('%(asctime)s-%(process)d-%(thread)d-%(module)s-%(funcName)s-%(levelname)s-'
                                      ':%(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    async def listening(self, callback):
        """
        callback with format {'header': dict; 'data': encoded data}
        :param callback:
        :return:
        """
        raise NotImplementedError

