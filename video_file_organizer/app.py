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
        self.config = ConfigHandler(self.config_dir, self.args)
        self.event = EventHandler()
        self.rule_book = RuleBookHandler(self.config_dir, self.event)

    def run(self):
        """This is the main function of the app. This requires the setup
        function to be run first before it will be able to run properly"""
        logger.debug("Running app")
        try:
            with yg.lockfile.FileLock(
                    os.path.join(tempfile.gettempdir(), 'vfolock'),
                    timeout=10):
                self.series_index = scan_series_dirs(self.config)
                self.scan_queue = scan_input_dir(self.config, self.rule_book)
                self.matched_queue = matcher(
                    self.scan_queue, self.event, self.series_index)
                transferer(self.matched_queue, self.event)
        except yg.lockfile.FileLockTimeout:
            logger.warning("FAILED LOCKFILE: " +
                           "The program must already be running")
