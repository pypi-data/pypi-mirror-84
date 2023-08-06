import asyncio
import pyxeed.pusher
from pyxeed.utils.exceptions import XeedTypeError, XeedDataSpecError
from pyxeed.listener.listeners.basic_listener import BasicListener


__all__ = ['Streamer']


class Streamer(pyxeed.pusher.Pusher):
    """
    Pull from extractor and push to messager
    """
    def __init__(self, listener=None, messager=None, translators=list()):
        super().__init__(messager=messager, translators=translators)
        if not listener:
            self.listener = BasicListener()
        elif isinstance(listener, pyxeed.listener.Listener):
            self.listener = listener
        else:
            self.logger.error("The Choosen Listener has a wrong Type")
            raise XeedTypeError("XED-000005")

    def callback(self, header: dict):
        data = header.pop('data')
        self.push_data(header, data)

    def stream_and_push(self):
        loop = asyncio.get_event_loop()
        tasks = [self.listener.listening(callback=self.callback)]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()




