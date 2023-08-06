import io
import logging

__all__ = ['Extractor']


class Extractor():
    def __init__(self):
        self.logger = logging.getLogger("Xeed.Extractor")
        if len(self.logger.handlers) == 0:
            formatter = logging.Formatter('%(asctime)s-%(process)d-%(thread)d-%(module)s-%(funcName)s-%(levelname)s-'
                                          ':%(message)s')
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def sniff_record_field(self, header_dict: dict):
        for key, value in header_dict.items():
            if isinstance(value, list):
                for u in value:
                    if isinstance(u, dict):
                        return key

    def init_extractor(self, data_encode, data_format, data_store, **kwargs):
        self.header = {'data_encode': data_encode,
                       'data_format': data_format,
                       'data_store': data_store}
        if 'data_header_spec' in kwargs:
            self.header['data_header_spec'] = kwargs['data_header_spec']
        elif 'data_body_spec' in kwargs:
            self.header['data_body_spec'] = kwargs['data_body_spec']

    def extract(self):
        """

        :return:
        [0] Metadata
        [1] Data or IO handlers
        """
        raise NotImplementedError
