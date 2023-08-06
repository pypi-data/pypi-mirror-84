import io
import json
import logging
from functools import reduce
from pyxeed.utils.exceptions import XeedFormatError

__all__ = ['Formatter']


class Formatter():
    def __init__(self):
        self.support_formats = ['list', 'record']
        self.logger = logging.getLogger("Xeed.Fromatter")
        formatter = logging.Formatter('%(asctime)s-%(process)d-%(thread)d-%(module)s-%(funcName)s-%(levelname)s-'
                                      ':%(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def _format_to_record(self, data_or_io, from_format, **kwargs):
        """
        Format data to record format
        Input must be decoded to 'flat' or 'BufferedIO'
        :param data:
        :param format:
        :return:
        """
        if isinstance(data_or_io, bytes):
            yield json.loads(data_or_io.decode())
        elif isinstance(data_or_io, str):
            yield json.loads(data_or_io)
        # IO Termination
        elif isinstance(data_or_io, io.BufferedIOBase):
            yield json.load(data_or_io)

    def list_to_record(self, data: dict):
        if not data:
            return list()
        line_nbs = [len(value) for key, value in data.items()]
        if len(set(line_nbs)) > 1:
            self.logger.error("list must have identical line numbers")
            raise XeedFormatError("XED-000008")
        return [{key: value[i] for key, value in data.items() if value[i] is not None} for i in range(line_nbs[0])]

    def formatter(self, data_or_io, from_format, **kwargs):
        if len(self.support_formats) == 0:
            raise NotImplementedError

        if not data_or_io:
            self.logger.warning("No data or IO found at {}".format(self.__class__.__name__))
            yield data_or_io

        if from_format not in self.support_formats:
            self.logger.error("Formatter of {} not found at {}".format(from_format, self.__class__.__name__))
            raise XeedFormatError("XED-000010")

        if not isinstance(data_or_io, (str, bytes, io.BufferedIOBase)):
            self.logger.error("Data type {} not supported".format(data_or_io.__class__.__name__))
            raise XeedFormatError("XED-000010")

        for output in self._format_to_record(data_or_io, from_format, **kwargs):
            for line in output:
                yield line
