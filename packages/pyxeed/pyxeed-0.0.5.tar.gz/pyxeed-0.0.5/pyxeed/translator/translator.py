__all__ = ['Translator']


class Translator():
    def __init__(self):
        self.spec_list = list()
        self.translate_method = None

    def init_translator(self, header: dict, data: list):
        raise NotImplementedError

    def get_translated_line(self, line: dict, **kwargs) -> dict:
        if not self.translate_method:
            raise NotImplementedError
        return self.translate_method(line, **kwargs)
