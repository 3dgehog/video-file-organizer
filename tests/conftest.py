import logging

from tests.fixtures import *  # noqa


logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)

fh_debug = logging.FileHandler('debug.log')
fh_debug.setLevel(logging.DEBUG)

fh_warning = logging.FileHandler('warning.log')
fh_warning.setLevel(logging.WARNING)

formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s:%(message)s')
fh_debug.setFormatter(formatter)
fh_warning.setFormatter(formatter)

logger.addHandler(fh_debug)
logger.addHandler(fh_warning)
