import logging
import sys
from typing import Optional, List

from video_file_organizer.config import Config, RuleBook
from video_file_organizer.app import App
from video_file_organizer.event import fire_event
from video_file_organizer.scheduler import scheduler
from video_file_organizer.rpyc_services import server
from video_file_organizer.webserver.server import WebServer


logger = logging.getLogger('vfo.manager')
manager: Optional['Manager'] = None


class Manager:
    def __init__(self, args: Optional[List[str]]):
        logger.debug("manager initializing...")

        global manager
        assert not manager
        manager = self

        self.scheduler = None
        self.webserver = None
        self.rpyc = None

        self.args = args
        self.config = None
        self.rulebook = None

        self.initialized = False
        self.initialize()

    def initialize(self):

        if self.initialized:
            raise RuntimeError(
                'Cannot call initialize on an already initialized manager.')

        fire_event('manager.initialize', self)
        self.config = Config(self.args)
        self.rulebook = RuleBook(self.args)

        if self.args.web:
            logger.debug('Starting scheduler...')
            if self.args.scheduler:
                scheduler.add_job(
                    self.start,
                    'interval',
                    minutes=self.config.schedule,
                    name='vfo')
                logger.info(
                    f"Scheduler Started! Running every {self.config.schedule} "
                    "minute(s)")
            scheduler.start()

            self.scheduler = scheduler

            self.webserver = WebServer()
            logger.debug('Starting webserver')
            self.webserver.start()

            try:
                logger.info("RPYC Server running")
                server.start()
            except (KeyboardInterrupt, SystemExit):
                pass
            finally:
                scheduler.shutdown()
                self.webserver.stop()

            sys.exit(0)

        if self.args.scheduler:
            scheduler.add_job(
                self.start,
                'interval',
                minutes=self.config.schedule,
                # args={'args': self.args},
                name='vfo')
            logger.info(
                f"Scheduler Started! Running every {self.config.schedule} "
                "minute(s)")
            scheduler.start()

            self.scheduler = scheduler

            try:
                logger.info("RPYC Server running")
                server.start()
            except (KeyboardInterrupt, SystemExit):
                pass
            finally:
                scheduler.shutdown()

            sys.exit(0)

    def start(self):
        logger.debug("Manager Started")

        app = App()
        app.setup(self.args)
        app.run()
