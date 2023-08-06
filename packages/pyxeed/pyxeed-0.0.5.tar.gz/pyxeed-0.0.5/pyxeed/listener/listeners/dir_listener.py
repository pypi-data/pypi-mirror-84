import os
import re
import json
import asyncio
from ..listener import Listener
from pyxeed.utils.exceptions import XeedTypeError
from pyxeed.extractor.extractors.dir_extractor import DirExtractor

class DirListener(Listener):
    """
    get file -> callback and remove
    """
    def __init__(self, extractor: DirExtractor):
        super().__init__()
        if isinstance(extractor, DirExtractor):
            self.extractor = extractor
        else:
            self.logger.error("The Choosen Extractor has a wrong Type")
            raise XeedTypeError("XED-000001")

    def set_dir_paths(self, dir_path: str):
        self.extractor.dir_path = dir_path

    async def listening(self, callback):
        while True:
            del_list = [f for f in os.listdir(self.extractor.dir_path)]
            if del_list:
                for extr_data in self.extractor.extract():
                    assert isinstance(extr_data, dict)
                    header = extr_data['header']
                    data = extr_data['data']
                    info = extr_data['extract_info']
                    callback(header, data, info)
                for del_item in del_list:
                    os.remove(os.path.join(self.extractor.dir_path, del_item))
            await asyncio.sleep(1)