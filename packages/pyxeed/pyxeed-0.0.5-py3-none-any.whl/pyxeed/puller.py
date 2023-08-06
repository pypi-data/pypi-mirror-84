from pyxeed.utils.core import MESSAGE_SIZE, FILE_SIZE
from pyxeed.utils.exceptions import XeedTypeError, XeedDataSpecError
from pyxeed.xeed import Xeed
from pyxeed.pusher import Pusher
from pyxeed.extractor.extractor import Extractor
from pyxeed.extractor.extractors.dir_extractor import DirExtractor

__all__ = ['Puller']


class Puller(Xeed):
    """
    Pull from extractor and Push
    """
    def __init__(self, extractor, pusher):
        super().__init__()
        if isinstance(extractor, Extractor):
            self.extractor = extractor
        else:
            self.logger.error("The Choosen Extractor has a wrong Type")
            raise XeedTypeError("XED-000001")

        if isinstance(pusher, Pusher):
            self.pusher = pusher
        else:
            self.logger.error("The Choosen Pusher has a wrong Type")
            raise XeedTypeError("XED-000015")

    def pull_and_push(self, topic_id, table_id, aged, start_seq, message_size=MESSAGE_SIZE, file_size=FILE_SIZE,
                      **kwargs):
        """

        :param topic_id:
        :param table_id:
        :param aged:
        :param start_seq:
        :param message_size:
        :param file_size:
        :param kwargs: 'age' and 'end_age' for aged documents
        :return:
        """
        header, data, cur_age, cur_start_seq = dict(), list(), 0, ''
        for extr_data in self.extractor.extract():
            assert isinstance(extr_data, dict)
            # Start sending data to make a send at last
            if header:
                cur_age, cur_start_seq, last_header = self.pusher.push_data(header, data, message_size, file_size)
            # Header construction
            header = extr_data['header']
            header['topic_id'] = topic_id
            header['table_id'] = table_id
            # Data construction
            data = extr_data['data']
            # Data send case 1: header
            if extr_data['extract_info']['type'] == 'header':
                header['aged'] = aged
                header['age'] = 1
                header['start_seq'] = start_seq
            else:
                header.pop('aged', None)
                # Data send case 2: Aged
                if aged:
                    header['start_seq'] = start_seq
                    if 'age' not in kwargs and cur_age == 0:
                        header['age'] = 2
                    elif 'age' in kwargs and cur_age == 0:
                        header['age'] = kwargs['age']
                    else:
                        header['age'] = last_header.get('end_age', last_header['age']) + 1
                # Data send case 3: Normal
                else:
                    header['start_seq'] = str(int(last_header['start_seq']) + 1)
            # Last push, end_age might be necessary
            if 'end_age' in kwargs and extr_data['extract_info']['type'] != 'header':
                header['end_age'] = kwargs['end_age']
            self.pusher.push_data(header, data, message_size, file_size)
