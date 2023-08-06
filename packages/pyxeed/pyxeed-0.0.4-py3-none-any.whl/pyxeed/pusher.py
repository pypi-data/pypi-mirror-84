import pyinsight
from pyinsight.messager.messagers.dummy_messager import DummyMessager
import pyxeed
from pyxeed.utils.exceptions import XeedTypeError, XeedDataSpecError


__all__ = ['Pusher']

class Pusher(pyxeed.xeed.Xeed):
    """
    Push directly to messager
    """
    def __init__(self, messager=None, translators=list()):
        super().__init__(translators=translators)
        # Messager Initialization
        if not messager:
            self.messager = DummyMessager()
        elif isinstance(messager, pyinsight.messager.Messager):
            self.messager = messager
        else:
            self.logger.error("The Choosen Messenger has a wrong Type")
            raise XeedTypeError("XED-000002")

    def push_data(self, header, data):
        # Step 1: Get the correct translator
        if header.get('data_spec', ''):
            active_translator = self.translators.get(header['data_spec'], None)
        else:
            active_translator = self.translators.get('x-i-a')
        if not active_translator:
            self.logger.error("No translator for data_spec {}".format(header['data_spec']))
            raise XeedDataSpecError("XED-000004")
        # Step 2: Message Preparation
        if self.messager.blob_support:
            msg_data = active_translator.get_encode_data(data, header['data_encode'], 'gzip', header)
            header['data_encode'] = 'gzip'
        else:
            msg_data = active_translator.get_encode_data(data, header['data_encode'], 'b64g', header)
            header['data_encode'] = 'b64g'
        header['data_spec'] = 'x-i-a'
        # Step 3: Send message
        self.messager.publish(header['topic_id'], header, msg_data)