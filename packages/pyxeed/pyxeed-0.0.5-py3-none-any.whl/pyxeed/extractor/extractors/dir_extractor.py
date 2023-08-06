import os
import re
import json
from ..extractor import Extractor

class DirExtractor(Extractor):
    """
    Extract all files from a directory with the following default setting
    * Table structure file will be first file which doesn't start with a number
    * Data filename should contains only number.
    * Age number deducted by file name ######.json
    """
    def init_extractor(self, data_encode, data_format, data_store, **kwargs):
        super().init_extractor(data_encode, data_format, data_store)
        self.dir_path = kwargs['dir_path']
        self.extension = kwargs['extension']
        if 'header_regex' in kwargs:
            re.compile(kwargs['header_regex'])
        else:
            self.header_file_regex = re.compile(r'^\D.*\.' + re.escape(self.extension) + r'$')
        self.data_file_regex = re.compile(r'^[0-9]*.' + re.escape(self.extension) + r'$')

    def extract(self):
        result = dict()
        # Step 1: get header file
        for filename in os.listdir(self.dir_path):
            if self.header_file_regex.search(filename):
                with open(os.path.join(self.dir_path, filename)) as file_io:
                    try:
                        header_content = json.load(file_io)
                    except Exception as e:
                        self.logger.warning("{} is not a json file".format(filename))
                        continue
                    result['header'] = self.header.copy()
                    if 'data_header_spec' in result['header']:
                        result['header']['data_spec'] = result['header'].pop('data_header_spec')
                        result['header'].pop('data_body_spec', None)
                        result['data'] = header_content.pop('data')
                    else:
                        field_key = self.sniff_record_field(header_content)
                        if not field_key:
                            self.logger.warning("field definition not found at {}".format(filename))
                            continue
                        result['data'] = header_content.pop(field_key)
                    result['header']['meta-data'] = header_content
                    result['header']['data_encode'] = 'body'
                    result['header']['data_format'] = 'record'
                    result['extract_info'] = {'type': 'header', 'table_id': filename,
                                              'fullname': os.path.join(self.dir_path, filename),
                                              'data_type': file_io.__class__.__name__}
                    yield result
                    break

        # Step 2: Get file one by one
        for filename in sorted(os.listdir(self.dir_path), key=lambda x: str(x).zfill(20)):
            if self.data_file_regex.search(filename):
                with open(os.path.join(self.dir_path, filename), 'rb') as file_io:
                    result['header'] = self.header.copy()
                    if 'data_body_spec' in result['header']:
                        result['header']['data_spec'] = result['header'].pop('data_body_spec')
                        result['header'].pop('data_header_spec', None)
                    result['data'] = file_io
                    result['extract_info'] = {'type': 'data', 'table_id': filename,
                                              'age_hint': int(filename.split('.')[0]),
                                              'fullname': os.path.join(self.dir_path, filename),
                                              'data_type': file_io.__class__.__name__}
                    yield result
