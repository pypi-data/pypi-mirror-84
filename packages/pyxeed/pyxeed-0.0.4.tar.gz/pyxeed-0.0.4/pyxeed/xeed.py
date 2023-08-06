import logging
import pyxeed
from pyxeed.utils.core import LOGGING_LEVEL
from pyxeed.utils.exceptions import XeedTypeError, XeedDataSpecError
from pyxeed.translator.translators import SapTranslator, XIATranslator

__all__ = ['Xeed']


class Xeed():
    def __init__(self, translators=list()):
        self.logger = logging.getLogger("Xeed")
        self.logger.setLevel(LOGGING_LEVEL)

        # Standard Translators
        self.translators = dict()
        xia_trans = XIATranslator()
        sap_trans = SapTranslator()
        for std_trans in [xia_trans, sap_trans]:
            for spec in std_trans.spec_list:
                self.translators[spec] = std_trans
        # Customized Translators (can overwrite standard ones)
        for cust_trans in translators:
            if isinstance(cust_trans, pyxeed.translator.Translator):
                for spec in cust_trans.spec_list:
                    self.translators[spec] = cust_trans
            else:
                self.logger.error("The Choosen Translator has a wrong Type")
                raise XeedTypeError("XED-000003")