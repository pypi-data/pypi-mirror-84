import os
import re
import json
import asyncio
from pyinsight.utils.core import encoder, get_current_timestamp
from ..listener import Listener
from pyxeed.extractor.extractors.basic_extractor import BasicExtractor

class BasicListener(Listener):
    """
    Watch a directory for the new file with the following default setting
    * Table structure will be first json file which doesn't start with a number
    * Data filename should contains only number.
    * Age number deducted by file name ######.json
    """
    def __init__(self):
        super().__init__()
        self.extractor = None

    def set_extractor(self, extractor: BasicExtractor):
        self.extractor = extractor

    async def listening(self, callback):
        if not isinstance(self.extractor, BasicExtractor):
            return
        while True:
            h_list = [f for f in os.listdir(self.extractor.source_dir) if self.extractor.header_file_regex.search(f)]
            header = self.extractor.get_table_header()
            if header:
                callback(header)
            d_list = [f for f in os.listdir(self.extractor.source_dir) if self.extractor.data_file_regex.search(f)]
            if self.extractor.aged:
                for data_item in self.extractor.get_aged_data():
                    callback(data_item)
            del_list = h_list + d_list
            for del_item in del_list:
                os.remove(os.path.join(self.extractor.source_dir, del_item))
            await asyncio.sleep(1)