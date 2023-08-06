import pyxeed.pusher
from pyxeed.utils.exceptions import XeedTypeError, XeedDataSpecError
from pyxeed.extractor.extractors.basic_extractor import BasicExtractor

__all__ = ['Puller']


class Puller(pyxeed.pusher.Pusher):
    """
    Pull from extractor and push to messager
    """
    def __init__(self, extractor=None, messager=None, translators=list()):
        super().__init__(messager=messager, translators=translators)
        if not extractor:
            self.extrator = BasicExtractor()
        elif isinstance(extractor, pyxeed.extractor.Extractor):
            self.extrator = extractor
        else:
            self.logger.error("The Choosen Extractor has a wrong Type")
            raise XeedTypeError("XED-000001")

    def pull_and_push(self):
        if self.extrator.aged:
            for header in self.extrator.get_aged_data():
                data = header.pop('data')
                self.push_data(header, data)
        else:
            for header in self.extrator.get_normal_data():
                data = header.pop('data')
                self.push_data(header, data)
