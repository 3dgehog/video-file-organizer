import os
import logging
import tempfile
import yg.lockfile

from video_file_organizer.handlers.config import ConfigHandler
from video_file_organizer.handlers.rule_book import RuleBookHandler
from video_file_organizer.models import OutputFolder, InputFolder
from video_file_organizer.utils import get_vfile_guessit, Matcher, \
    Transferer
from video_file_organizer.rules import rules_before_matching_vfile, \
    rules_before_transfering_vfile


logger = logging.getLogger('vfo.app')


class App:
    def __init__(self, config_dir: str, **kwargs):
        self.config_dir = config_dir

    def setup(self, **kwargs):
        """A function that starts up the app, it gets and executes the
        ConfigHandler, args and RuleBookHandler. This is
        run even before any of the searching and matching is done on the
        directory to make sure that all the configs are ready to go"""
        logger.debug("Setting up app")
        self.config = ConfigHandler(self.config_dir, **kwargs)
        self.rule_book = RuleBookHandler(self.config_dir)

    def run(self, **kwargs):
        """This is the main function of the app. This requires the setup
        function to be run first before it will be able to run properly"""
        logger.debug("Running app")
        try:
            with yg.lockfile.FileLock(
                    os.path.join(tempfile.gettempdir(), 'vfolock'),
                    timeout=10):

                self.output_folder = OutputFolder(self.config.series_dirs)
                self.input_folder = InputFolder(self.config.input_dir)

                matcher = Matcher(self.output_folder)

                with self.input_folder as ifolder:
                    for name, vfile in ifolder.iter_vfiles():
                        # Guessit
                        results = get_vfile_guessit(vfile=vfile)
                        if results is None:
                            ifolder.remove_vfile(name)
                            continue
                        vfile.edit(guessit=results)
                        # Rules from rule_book
                        results = self.rule_book.get_vfile_rules(vfile)
                        if results is None:
                            ifolder.remove_vfile(name)
                            continue
                        vfile.edit(rules=results)
                        # Apply rules before matcher
                        result = rules_before_matching_vfile(vfile)
                        vfile.edit(guessit=result)
                        # Matcher
                        results = matcher.get_vfile_match(vfile=vfile)
                        if results is None:
                            ifolder.remove_vfile(name)
                            continue
                        vfile.edit(name, match=results)
                        # Apply rules before transfering
                        transfer, guessit = rules_before_transfering_vfile(
                            vfile)
                        if transfer is None:
                            ifolder.remove_vfile(name)
                            continue
                        vfile.edit(transfer=transfer, guessit=guessit)
                # Transfer
                with Transferer() as transferer:
                    for name, vfile in self.input_folder.iter_vfiles():
                        transferer.transfer_vfile(vfile)

        except yg.lockfile.FileLockTimeout:
            logger.warning("Lockfile FAILED: " +
                           "The program must already be running")
