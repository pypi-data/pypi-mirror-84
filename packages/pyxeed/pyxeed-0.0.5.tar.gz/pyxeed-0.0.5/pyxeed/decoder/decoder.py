import io
import gzip
import base64
import logging
from pyxeed.utils.exceptions import XeedDecodeError

__all__ = ['Decoder']

class Decoder():
    def __init__(self):
        self.support_encodes = ['blob', 'flat', 'gzip', 'b64g']
        self.logger = logging.getLogger("Xeed.Decoder")
        formatter = logging.Formatter('%(asctime)s-%(process)d-%(thread)d-%(module)s-%(funcName)s-%(levelname)s-'
                                      ':%(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def basic_encoder(self, data, from_encode, to_encode):
        if from_encode not in ['blob', 'flat', 'gzip', 'b64g']:
            self.logger.error("Cannot decoder to {}".format(to_encode))
            raise XeedDecodeError("XED-000006")
        if to_encode not in ['blob', 'flat', 'gzip', 'b64g']:
            self.logger.error("Cannot decoder from {} with basic encoder".format(to_encode))
            raise XeedDecodeError("XED-000007")

        if from_encode == to_encode:
            yield data
        if from_encode == 'gzip' and to_encode == 'flat':
            yield gzip.decompress(data).decode()
        elif from_encode == 'b64g' and to_encode == 'flat':
            yield gzip.decompress(base64.b64decode(data.encode())).decode()
        elif from_encode == 'blob' and to_encode == 'flat':
            yield data.decode()
        elif from_encode == 'flat' and to_encode == 'b64g':
            yield base64.b64encode(gzip.compress(data.encode())).decode()
        elif from_encode == 'gzip' and to_encode == 'b64g':
            yield base64.b64encode(data).decode()
        elif from_encode == 'blob' and to_encode == 'b64g':
            yield base64.b64encode(gzip.compress(data)).decode()
        elif from_encode == 'flat' and to_encode == 'gzip':
            yield gzip.compress(data.encode())
        elif from_encode == 'b64g' and to_encode == 'gzip':
            yield base64.b64decode(data.encode())
        elif from_encode == 'blob' and to_encode == 'gzip':
            yield gzip.compress(data)
        elif from_encode == 'flat' and to_encode == 'blob':
            yield data.encode()
        elif from_encode == 'gzip' and to_encode == 'blob':
            yield gzip.decompress(data)
        elif from_encode == 'b64g' and to_encode == 'blob':
            yield gzip.decompress(base64.b64decode(data.encode()))

    def _encode_to_blob(self, data_or_io, from_encode, **kwargs):
        if isinstance(data_or_io, io.BufferedIOBase):
            if from_encode == 'blob':
                yield data_or_io
            elif from_encode == 'gzip':
                with gzip.GzipFile(fileobj=data_or_io) as f:
                    yield f
            else:
                # flat or b64g, terminating IO
                data_or_io = data_or_io.read().decode()
                for output in self.basic_encoder(data_or_io, from_encode, 'blob'):
                    yield output
        else:
            for output in self.basic_encoder(data_or_io, from_encode, 'blob'):
                yield output

    def decoder(self, data_or_io, from_encode, to_encode, **kwargs):
        """
        Decode data to the the final encode
        final encode must be one of [gzip, b64g, flat, blob]
        :param data:
        :param encode:
        :return:
        """
        if len(self.support_encodes) == 0:
            raise NotImplementedError

        if not data_or_io:
            self.logger.warning("No data or IO found at {}".format(self.__class__.__name__))
            yield data_or_io

        if from_encode not in self.support_encodes:
            self.logger.error("Decoder of {} not found at {}".format(from_encode, self.__class__.__name__))
            raise XeedDecodeError("XED-000007")

        if not isinstance(data_or_io, (str, bytes, io.BufferedIOBase)):
            self.logger.error("Data type {} not supported".format(data_or_io.__class__.__name__))
            raise XeedDecodeError("XED-000007")

        if to_encode not in ['blob', 'flat', 'gzip', 'b64g']:
            self.logger.error("Cannot decoder to {}".format(to_encode))
            raise XeedDecodeError("XED-000006")

        # Blob type
        if from_encode in ['blob', 'flat', 'gzip', 'b64g']:
            if to_encode == 'blob':
                for output in self._encode_to_blob(data_or_io, from_encode):
                    yield output
            else:
                # Terminating
                if isinstance(data_or_io, io.BufferedIOBase):
                    if from_encode in ['flat', 'b64g']:
                        data_or_io = data_or_io.read().decode()
                    else:
                        data_or_io = data_or_io.read()
                for output in self.basic_encoder(data_or_io, from_encode, to_encode):
                    yield output
        else:
            for output in self._encode_to_blob(data_or_io, from_encode, **kwargs):
                if to_encode == 'blob':
                    yield output
                elif isinstance(output, io.BufferedIOBase):
                    output = output.read()
                    yield self.basic_encoder(output, 'blob', to_encode)
                else:
                    yield self.basic_encoder(output, 'blob', to_encode)

