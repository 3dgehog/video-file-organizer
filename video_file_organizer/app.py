import os
import logging

from video_file_organizer.configs import ConfigHandler
from video_file_organizer.events import EventHandler
from video_file_organizer.rules.rule_book import RuleBookHandler
from video_file_organizer.matcher import matcher
from video_file_organizer.scanners import scan_input_dir, scan_series_dirs

CONFIG_DIR = os.path.join(os.environ['HOME'], '.config/video_file_organizer/')

# Create logger for app
logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('debug.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s:%(levelname)s:%(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


class App:
    def __init__(self, config_dir=CONFIG_DIR, args=None) -> None:
        self.config_dir = config_dir
        self.args = args

    def setup(self):
        logger.info("Setting up App")
        self.config = ConfigHandler(self)
        self.config.args = self.args
        self.event = EventHandler(self)
        self.rule_book = RuleBookHandler(self)

    def run(self):
        logger.info("Running App")
        self.series_index = scan_series_dirs(self)
        self.scan_queue = scan_input_dir(self)
        self.matched_queue = matcher(self)

    def _requirements(self, requirements: list):
        for require in requirements:
            if require not in dir(self):
                raise AttributeError(
                    "Missing attributes {} in app".format(require))
