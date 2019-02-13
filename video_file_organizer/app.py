import os
import logging
import tempfile
import yg.lockfile

from video_file_organizer.handlers.config import ConfigHandler
from video_file_organizer.handlers.event import EventHandler
from video_file_organizer.handlers.rule_book import RuleBookHandler
from video_file_organizer.matcher import matcher
from video_file_organizer.scanners import scan_input_dir, scan_series_dirs
from video_file_organizer.transferer import transferer

CONFIG_DIR = os.path.join(os.environ['HOME'], '.config/video_file_organizer/')


logger = logging.getLogger('app')


class App:
    def __init__(self, config_dir=CONFIG_DIR, args=None) -> None:
        self.config_dir = config_dir
        self.args = args

    def setup(self):
        """A function that starts up the app, it gets and executes the
        ConfigHandler, args, EventHandler and RuleBookHandler. This is
        run even before any of the searching and matching is done on the
        directory to make sure that all the configs are ready to go"""
        logger.debug("Setting up app")
        self.config = ConfigHandler(self)
        self.config.args = self.args
        self.event = EventHandler(self)
        self.rule_book = RuleBookHandler(self)

    def run(self):
        """This is the main function of the app. This requires the setup
        function to be run first before it will be able to run properly"""
        logger.debug("Running app")
        try:
            with yg.lockfile.FileLock(
                    os.path.join(tempfile.gettempdir(), 'vfolock'),
                    timeout=10):
                self.series_index = scan_series_dirs(self)
                self.scan_queue = scan_input_dir(self)
                self.matched_queue = matcher(self)
                transferer(self)
        except yg.lockfile.FileLockTimeout:
            logger.warning("FAILED LOCKFILE: " +
                           "The program must already be running")

    def _requirements(self, requirements: list):
        """A simple function used by all of the application to make sure
        that the functions that run have their requirements ready"""
        for require in requirements:
            if require not in dir(self):
                raise AttributeError(
                    "Missing attributes {} in app".format(require))
