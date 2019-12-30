import os
import logging
import tempfile
import yg.lockfile

from video_file_organizer.handlers.config import ConfigHandler
from video_file_organizer.handlers.rule_book import RuleBookHandler
from video_file_organizer.settings import CONFIG_DIR
from video_file_organizer.models import OutputFolder, InputFolder
from video_file_organizer.utils import get_vfile_guessit, Matcher


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
        self.rule_book = RuleBookHandler(self.config_dir)

    def run(self):
        """This is the main function of the app. This requires the setup
        function to be run first before it will be able to run properly"""
        logger.debug("Running app")
        try:
            with yg.lockfile.FileLock(
                    os.path.join(tempfile.gettempdir(), 'vfolock'),
                    timeout=10):

                self.output_folder = OutputFolder(self.config.series_dirs)
                self.input_folder = InputFolder(self.config.input_dir)

                # Add guessit match to vfile
                for name, vfile in self.input_folder.iterate_vfiles():
                    results = get_vfile_guessit(vfile=vfile)
                    if results is None:
                        self.input_folder.remove_vfile(name)
                        continue
                    self.input_folder.edit_vfile(
                        name, guessit=results)

                # Add rules from rule_book
                for name, vfile in self.input_folder.iterate_vfiles():
                    rules = self.rule_book.get_vfile_rules(vfile)
                    if rules is None:
                        self.input_folder.remove_vfile(name)
                        continue
                    self.input_folder.edit_vfile(
                        name, rules=rules)

                # Match to output folder
                matcher = Matcher(self.output_folder)
                for name, vfile in self.input_folder.iterate_vfiles():
                    results = matcher.get_vfile_match(vfile=vfile)
                    if results is None:
                        self.input_folder.remove_vfile(name)
                        continue
                    self.input_folder.edit_vfile(name, match=results)

        except yg.lockfile.FileLockTimeout:
            logger.warning("FAILED LOCKFILE: " +
                           "The program must already be running")
