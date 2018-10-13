import os

from video_file_organizer.configs import ConfigHandler
from video_file_organizer.events import EventHandler
from video_file_organizer.rules.rule_book import RuleBookHandler
from video_file_organizer.matcher import matcher
from video_file_organizer.scanners import scan_input_dir, scan_series_dirs

CONFIG_DIR = os.path.join(os.environ['HOME'], '.config/video_file_organizer/')


class App:
    def __init__(self, config_dir=CONFIG_DIR, args=None) -> None:
        self.config_dir = config_dir
        self.config = ConfigHandler(self)
        self.config.args = args
        self.event = EventHandler(self)
        self.rule_book = RuleBookHandler(self)

    def run(self):
        self.series_index = scan_series_dirs(self)
        self.scan_queue = scan_input_dir(self)
        self.matched_queue = matcher(self)

    def _requirements(self, requirements: list):
        for require in requirements:
            if require not in dir(self):
                raise AttributeError(
                    "Missing attributes {} in app".format(require))
