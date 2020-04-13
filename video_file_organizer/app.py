import os
import logging
import tempfile
import yg.lockfile

from typing import Union

from video_file_organizer.config import setup_config_dir
from video_file_organizer.config.config_file import ConfigFile
from video_file_organizer.handlers.rule_book import RuleBookHandler
from video_file_organizer.models import OutputFolder, InputFolder
from video_file_organizer.utils import get_vfile_guessit, Matcher, \
    Transferer
from video_file_organizer.rules import rules_before_matching_vfile, \
    rules_before_transfering_vfile


logger = logging.getLogger('vfo.app')


class App:
    def setup(
            self,
            config_dir: Union[str, None] = None,
            create: bool = False):

        logger.debug("Setting up app")

        self.config_dir = setup_config_dir(
            create=create,
            path=config_dir)

        config_file_path = os.path.join(
            self.config_dir, 'config.yaml')

        self.config = ConfigFile(config_file_path, create=create)
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
