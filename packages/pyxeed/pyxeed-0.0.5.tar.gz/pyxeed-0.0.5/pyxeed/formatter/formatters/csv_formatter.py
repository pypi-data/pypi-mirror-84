import io
import csv
import codecs
import json
import gzip
from pyxeed.utils.exceptions import XeedFormatError
from ..formatter import Formatter

class CSVFormatter(Formatter):
    def __init__(self):
        super().__init__()
        self.support_formats = ['csv']

    def _format_to_record(self, data_or_io, from_format, **kwargs):
        if isinstance(data_or_io, io.BufferedIOBase):
            StreamReader = codecs.getreader('utf-8')
            reader_io = StreamReader(data_or_io)
        elif isinstance(data_or_io, bytes):
            reader_io = io.StringIO(data_or_io.decode())
        elif isinstance(data_or_io, str):
            reader_io = io.StringIO(data_or_io)
        else:
            self.logger.error("Data type {} not supported".format(data_or_io.__class__.__name__))
            raise XeedFormatError("XED-000010")
        counter, chunk = 0, list()
        dialect = csv.Sniffer().sniff(reader_io.read(4096))
        reader_io.seek(0)
        reader = csv.DictReader(reader_io, dialect=dialect)
        for row in reader:
            counter += 1
            chunk.append(dict(row))
            if counter % 64 == 0:
                yield chunk
                chunk = list()
        yield chunk
