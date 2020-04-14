import os
import logging
import tempfile
import yg.lockfile

from typing import Union

from video_file_organizer.config import ConfigDirectory
from video_file_organizer.models import OutputFolder, InputFolder
from video_file_organizer.utils import get_vfile_guessit, \
    OutputFolderMatcher, Transferer, RuleBookMatcher
from video_file_organizer.rules import rules_before_matching_vfile, \
    rules_before_transfering_vfile


logger = logging.getLogger('vfo.app')


class App:
    def setup(
            self, config_dir: Union[str, None] = None, create: bool = False):

        logger.debug("Setting up app")

        self.configdir = ConfigDirectory(config_dir, create)

        self.config = self.configdir.configfile
        self.rulebook = self.configdir.rulebookfile

    def run(self, **kwargs):
        """This is the main function of the app. This requires the setup
        function to be run first before it will be able to run properly"""
        logger.debug("Running app")
        try:
            with yg.lockfile.FileLock(
                    os.path.join(tempfile.gettempdir(), 'vfolock'),
                    timeout=10):

                self.output_folder = OutputFolder(self.config.series_dirs)
                self.input_folder = InputFolder(
                    self.config.input_dir,
                    videoextensions=self.config.videoextensions)

                folder_matcher = OutputFolderMatcher(self.output_folder)
                rulebook_matcher = RuleBookMatcher(self.rulebook)

                with self.input_folder as ifolder:
                    for name, vfile in ifolder.iter_vfiles():
                        # Guessit
                        results = get_vfile_guessit(vfile=vfile)
                        if results is None:
                            ifolder.remove_vfile(name)
                            continue
                        vfile.edit(guessit=results)
                        # Rules from rule_book
                        results = rulebook_matcher.get_vfile_rules(vfile)
                        if results is None:
                            ifolder.remove_vfile(name)
                            continue
                        vfile.edit(rules=results)
                        # Apply rules before matcher
                        result = rules_before_matching_vfile(vfile)
                        vfile.edit(guessit=result)
                        # Matcher
                        results = folder_matcher.get_vfile_match(vfile=vfile)
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
