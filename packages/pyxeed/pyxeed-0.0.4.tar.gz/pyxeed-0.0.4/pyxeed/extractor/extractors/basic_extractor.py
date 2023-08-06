import os
import re
import json
from pyinsight.utils.core import encoder, get_current_timestamp
from ..extractor import Extractor

class BasicExtractor(Extractor):
    """
    Extract all json files a directory with the following default setting
    * Table structure will be first json file which doesn't start with a number
    * Data filename should contains only number.
    * Age number deducted by file name ######.json
    """
    def __init__(self):
        super().__init__()
        self.data_encode = 'flat'
        self.data_format = 'record'
        self.data_store = 'body'
        self.source_dir = os.path.join(os.path.expanduser('~'), 'xeed-extractor')
        self.header_file_regex = re.compile(r'^\D.*\.json$')
        self.data_file_regex = re.compile(r'^[0-9]*.json$')

    def init_extractor(self, **kwargs):
        super().init_extractor(**kwargs)
        for key, value in kwargs.items():
            if key == 'source_dir':
                self.source_dir = value
            elif key == 'header_file_regex':
                self.header_file_regex = re.compile(value)
            elif key == 'data_file_regex':
                self.data_file_regex = re.compile(value)
            elif key == 'aged':
                self.aged = value

    def get_aged_data(self):
        """
        Get Table Data
        :return: dictionary with 'age', 'end_age' and 'data'.
        """
        data_list = [f for f in os.listdir(self.source_dir) if self.data_file_regex.search(f)]
        data_list = sorted(data_list, key=lambda x:int(x[:-5]))
        data_file, start_age, content = '', 0, None
        start_seq = get_current_timestamp()
        for filename in os.listdir(self.source_dir):
            if self.header_file_regex.search(filename):
                data_value = list()
                with open(os.path.join(self.source_dir, filename)) as f:
                    content = json.load(f)
                for key, value in content.items():
                    if isinstance(value, list):
                        for u in value:
                            if isinstance(u, dict):
                                data_value = value
                                break
                        if data_value:
                            content.pop(key)
                            result = self.update_data_info(dict())
                            result['start_seq'] = start_seq
                            result['aged'] = self.aged
                            result['age'] = 1
                            result['meta_data'] = encoder(json.dumps(content), 'flat', 'b64g')
                            result['data'] = encoder(json.dumps(data_value), 'flat', self.data_encode)
                            result['data_spec'] = self.data_header_spec
                            yield result
                            break

        for data_file in data_list:
            with open(os.path.join(self.source_dir, data_file)) as f:
                if start_age and start_age > 1:
                    result = self.update_data_info(dict())
                    result['age'] = start_age
                    result['end_age'] = int(data_file[:-5]) - 1
                    result['data'] = content
                    result['start_seq'] = start_seq
                    result['data_spec'] = self.data_body_spec
                    yield result
                start_age = int(data_file[:-5])
                content = f.read()
        if start_age and start_age > 1:
            result = self.update_data_info(dict())
            result['age'] = start_age
            result['end_age'] = int(data_file[:-5]) - 1
            result['data'] = content
            result['start_seq'] = start_seq
            result['data_spec'] = self.data_body_spec
            yield result

    def get_normal_data(self):
        for result in self.get_aged_data():
            if result['age'] != 1:
                result.pop('age', None)
                result.pop('end_age', None)
                result['start_seq'] = get_current_timestamp()
            yield result