import io
import json
import gzip
import pyxeed
from .xeed import Xeed
from pyxeed.utils.core import MESSAGE_SIZE, FILE_SIZE
from pyxeed.sender.sender import Sender
from pyxeed.sender.senders.dummy_sender import DummySender
from pyxeed.utils.exceptions import XeedTypeError, XeedDataSpecError

__all__ = ['Pusher']


class Pusher(Xeed):
    """
    Push directly to messager
    """
    def __init__(self, sender=None, decoders=list(), formatters=list(), translators=list()):
        super().__init__(decoders=decoders, formatters=formatters, translators=translators)
        # Sender initialization
        if not sender:
            self.sender = DummySender()
        elif isinstance(sender, Sender):
            self.sender = sender
        else:
            self.logger.error("The Choosen Sender has a wrong Type")
            raise XeedTypeError("XED-000002")

    def _incr_age_start_seq(self, age: int, start_seq: str, header: dict, new_age: bool):
        if age == 1:
            pass
        elif 'age' in header:
            age = age + 1
            if new_age:
                header['age'] = str(age)
                header.pop('end_age', 0)
            else:
                header['end_age'] = str(age)
        else:
            start_seq = str(int(start_seq) + 1)
            header['start_seq'] = start_seq
        return age, start_seq, header

    def push_data(self, header, data_or_io, message_size=MESSAGE_SIZE, file_size=FILE_SIZE):
        # Step 1: Check Get decoder, formatter and translator
        if not all(k in header for k in ['start_seq', 'data_encode', 'data_format', 'data_store']):
            raise XeedDataSpecError("XED-000014")

        active_decoder = self.decoders.get(header['data_encode'])
        if not active_decoder:
            self.logger.error("No decoder for encode {}".format(header['data_encode']))
            raise XeedDataSpecError("XED-000012")

        active_formatter = self.formatters.get(header['data_format'])
        if not active_formatter:
            self.logger.error("No formatter for format {}".format(header['data_format']))
            raise XeedDataSpecError("XED-000013")

        if header.get('data_spec', ''):
            active_translator = self.translators.get(header['data_spec'], None)
        else:
            active_translator = self.translators.get('x-i-a')
        if not active_translator:
            self.logger.error("No translator for data_spec {}".format(header['data_spec']))
            raise XeedDataSpecError("XED-000004")
        active_translator.init_translator(header, data_or_io)
        if 'data_spec' not in header:
            header['data_spec'] = 'x-i-a'

        # Send size definition (by message_size or by file_size)
        if self.sender.file_client:
            send_by_message = False
        else:
            send_by_message = True
        chunk_size = message_size // 8

        # Loop the data
        age, end_age, start_seq = int(header.get('age', 0)), int(header.get('end_age', 0)), header.get('start_seq', '')
        chunk_number, raw_size, data_io, zipped_size, zipped_io, age_size = 0, 0, None, 0, None, 0
        header.pop('end_age', None)
        # Step 3.1 Decoder
        for decoded_blob in active_decoder.decoder(data_or_io, header['data_encode'], 'blob'):
            # Step 3.2: Formatter
            for raw_line in active_formatter.formatter(decoded_blob, header['data_format']):
                # Step 3.3: Translator
                result_line = active_translator.get_translated_line(raw_line, age=age, start_seq=start_seq)
                json_line = json.dumps(result_line)
                # Step 3.4.1: IO Initialization
                if not data_io:
                    data_io = io.BytesIO()
                    zipped_io = gzip.GzipFile(mode='wb', fileobj=data_io)
                    zipped_io.write(('[' + json_line).encode())
                else:
                    zipped_io.write((',' + json_line).encode())
                raw_size += (len(json_line) + 1)
                # Chunk check :
                cur_chunk_number = raw_size // chunk_size
                if cur_chunk_number != chunk_number:
                    chunk_number = cur_chunk_number
                    zipped_io.flush()
                    zipped_size = data_io.getbuffer().nbytes
                    # Message Age / Start_seq changes
                    # Case 1: Send by message or by file
                    if zipped_size >= message_size and send_by_message or raw_size >= file_size and not send_by_message:
                        zipped_io.write(']'.encode())
                        zipped_io.close()
                        self.sender.send(header, data_io.getvalue())
                        age, start_seq, header = self._incr_age_start_seq(age, start_seq, header, True)
                        chunk_number, raw_size, data_io, zipped_size, zipped_io, age_size = 0, 0, None, 0, None, 0
                    # Case 2: Just a age number
                    elif zipped_size - age_size > message_size:
                        age, start_seq, header = self._incr_age_start_seq(age, start_seq, header, False)
                        age_size = zipped_size

        # Last action -> send remain data -> re-add end age if necessary
        if age < end_age:
            header['end_age'] = str(end_age)
        zipped_io.write(']'.encode())
        zipped_io.close()
        self.sender.send(header, data_io.getvalue())

        return age, start_seq, header


