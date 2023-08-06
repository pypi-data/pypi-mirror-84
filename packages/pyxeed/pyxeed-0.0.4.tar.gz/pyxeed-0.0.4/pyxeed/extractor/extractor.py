import logging

__all__ = ['Extractor']


class Extractor():
    def __init__(self):
        self.logger = logging.getLogger("Xeed.Extractor")
        self.topic_id = ''
        self.table_id = ''
        self.data_encode = ''
        self.data_format = ''
        self.data_header_spec = ''
        self.data_body_spec = ''
        self.data_store = ''
        self.aged = False
        if len(self.logger.handlers) == 0:
            formatter = logging.Formatter('%(asctime)s-%(process)d-%(thread)d-%(module)s-%(funcName)s-%(levelname)s-'
                                          ':%(message)s')
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def init_extractor(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'topic_id':
                self.topic_id = value
            elif key == 'table_id':
                self.table_id = value

    def update_data_info(self, header: dict) -> dict:
        header['topic_id'] = self.topic_id
        header['table_id'] = self.table_id
        header['data_encode'] = self.data_encode
        header['data_format'] = self.data_format
        header['data_store'] = self.data_store
        return header

    def get_table_header(self):
        pass

    def get_aged_data(self):
        pass

    def get_normal_data(self):
        pass

