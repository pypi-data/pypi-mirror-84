import asyncio
from pyxeed.utils.core import MESSAGE_SIZE, FILE_SIZE, get_current_timestamp
from pyxeed.utils.exceptions import XeedTypeError, XeedDataSpecError
from pyxeed.xeed import Xeed
from pyxeed.pusher import Pusher
from pyxeed.utils.exceptions import XeedTypeError, XeedDataSpecError
from pyxeed.extractor.extractor import Extractor
from pyxeed.listener.listener import Listener

__all__ = ['Streamer']


class Streamer(Xeed):
    """
    Pull from extractor and push to messager
    """
    def __init__(self, topic_id, listeners, pusher):
        super().__init__()
        self.topic_id = topic_id
        self.message_size = MESSAGE_SIZE
        self.file_size = FILE_SIZE
        self.table_id_conf = dict()
        if isinstance(pusher, Pusher):
            self.pusher = pusher
        else:
            self.logger.error("The Choosen Pusher has a wrong Type")
            raise XeedTypeError("XED-000015")

        self.listeners = list()
        for listener in listeners:
            if isinstance(listener, Listener):
                self.listeners.append(listener)
            else:
                self.logger.error("The Choosen Listener has a wrong Type")
                raise XeedTypeError("XED-00005")

    def init_streamer(self, table_id_conf, message_size=MESSAGE_SIZE, file_size=FILE_SIZE):
        self.message_size = message_size
        self.file_size = file_size

    def callback(self, header, data, info):
        # Destination Configuration
        header['topic_id'] = self.topic_id
        if info.get('table_id', '') in self.table_id_conf:
            header['table_id'] = self.table_id_conf[info['table_id']]
        if info['type'] == header:
            header['age'] = 1
        # Sequence Control
        header['start_seq'] = get_current_timestamp()
        self.pusher.push_data(header, data, self.message_size, self.file_size)

    def stream_and_push(self):
        loop = asyncio.get_event_loop()
        tasks = [listener.listening(callback=self.callback) for listener in self.listeners]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()




