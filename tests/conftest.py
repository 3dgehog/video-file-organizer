import logging

from tests.fixtures import *  # noqa


logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)

ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s:%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
