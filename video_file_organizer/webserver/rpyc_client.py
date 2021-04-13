import time
import rpyc
import sys
import logging

logger = logging.getLogger('vfo.rpyc cli')


class RPYCClient:
    def __init__(self, bind='localhost', port=2324):
        self.bind = bind
        self.port = port
        self._conn = None

    @property
    def conn(self):
        while True:
            try:
                logger.debug('Trying to connect to rpyc server...')
                self._conn = rpyc.connect(self.bind, self.port)
                logger.debug('Connected to rpyc server!')
                return self._conn
            except ConnectionRefusedError:
                time.sleep(5)
            except Exception:
                logger.warning("Unexpected error:", sys.exc_info()[0])
                raise
