import logging
from pyxeed.utils.core import LOGGING_LEVEL
from pyxeed.utils.exceptions import XeedTypeError, XeedDataSpecError
from pyxeed.decoder.decoder import Decoder
from pyxeed.formatter.formatter import Formatter
from pyxeed.translator.translator import Translator
from pyxeed.decoder.decoders import ZipDecoder
from pyxeed.formatter.formatters import CSVFormatter
from pyxeed.translator.translators import SapTranslator, XIATranslator

__all__ = ['Xeed']


class Xeed():
    def __init__(self, decoders=list(), formatters=list(), translators=list()):
        self.logger = logging.getLogger("Xeed")
        self.logger.setLevel(LOGGING_LEVEL)

        # Standard Decoders
        self.decoders = dict()
        xia_decoder = Decoder()
        zip_decoder = ZipDecoder()
        for std_decoder in [xia_decoder, zip_decoder]:
            for encode in std_decoder.support_encodes:
                self.decoders[encode] = std_decoder
        # Customized Decoders (can overwrite standard ones)
        for cust_decoder in decoders:
            if isinstance(cust_decoder, Decoder):
                for encode in cust_decoder.support_encodes:
                    self.decoders[encode] = cust_decoder
            else:
                self.logger.error("The Choosen Decoder has a wrong Type")
                raise XeedTypeError("XED-000012")

        # Standard Formatters
        self.formatters = dict()
        xia_formatter = Formatter()
        csv_formatter = CSVFormatter()
        for std_formatter in [xia_formatter, csv_formatter]:
            for format in std_formatter.support_formats:
                self.formatters[format] = std_formatter
        # Customized Formatters (can overwrite standard ones)
        for cust_formatter in formatters:
            if isinstance(cust_formatter, Formatter):
                for format in cust_formatter.support_formats:
                    self.formatters[format] = cust_formatter
            else:
                self.logger.error("The Choosen formatter has a wrong Type")
                raise XeedTypeError("XED-000013")

        # Standard Translators
        self.translators = dict()
        xia_trans = XIATranslator()
        sap_trans = SapTranslator()
        for std_trans in [xia_trans, sap_trans]:
            for spec in std_trans.spec_list:
                self.translators[spec] = std_trans
        # Customized Translators (can overwrite standard ones)
        for cust_trans in translators:
            if isinstance(cust_trans, Translator):
                for spec in cust_trans.spec_list:
                    self.translators[spec] = cust_trans
            else:
                self.logger.error("The Choosen Translator has a wrong Type")
                raise XeedTypeError("XED-000003")
