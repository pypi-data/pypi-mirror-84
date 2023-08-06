import os
import datetime
import logging

MESSAGE_SIZE = os.environ.get('XEED_MESSAGE_SIZE', 2 ** 18)
FILE_SIZE = os.environ.get('XEED_FILE_SIZE', 2 ** 26)
LOGGING_LEVEL = os.environ.get('XEED_LOGGING_LEVEL', logging.WARNING)

def get_current_timestamp():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')