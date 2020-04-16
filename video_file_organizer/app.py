import os
import logging
import tempfile
import yg.lockfile

from typing import Union

from video_file_organizer.config import ConfigDirectory
from video_file_organizer.models import VideoCollection, FolderCollection
from video_file_organizer.matchers import OutputFolderMatcher, \
    RuleBookMatcher, MetadataMatcher
from video_file_organizer.transferer import Transferer
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

                output_folder = FolderCollection(self.config.series_dirs)
                input_folder = VideoCollection(
                    self.config.input_dir,
                    videoextensions=self.config.videoextensions)

                metadata_matcher = MetadataMatcher()
                rulebook_matcher = RuleBookMatcher(self.rulebook)
                folder_matcher = OutputFolderMatcher(output_folder)

                with input_folder as ifolder:
                    for vfile in ifolder:
                        # Guessit
                        metadata = metadata_matcher(vfile)
                        if metadata is None:
                            vfile.edit(valid=False)
                            continue
                        vfile.edit(metadata=metadata)
                        # Rules from rule_book
                        rules = rulebook_matcher(vfile)
                        if rules is None:
                            vfile.edit(valid=False)
                            continue
                        vfile.edit(rules=rules)
                        # Apply rules before matcher
                        metadata = rules_before_matching_vfile(vfile)
                        vfile.edit(metadata=metadata)
                        # Matcher
                        foldermatch = folder_matcher(vfile)
                        if foldermatch is None:
                            vfile.edit(valid=False)
                            continue
                        vfile.edit(foldermatch=foldermatch)
                        # Apply rules before transfering
                        transfer, metadata = rules_before_transfering_vfile(
                            vfile)
                        if transfer is None:
                            vfile.edit(valid=False)
                            continue
                        vfile.edit(transfer=transfer, metadata=metadata)
                # Transfer
                with Transferer() as transferer:
                    for vfile in input_folder:
                        transferer.transfer_vfile(vfile)

        except yg.lockfile.FileLockTimeout:
            logger.warning("Lockfile FAILED: " +
                           "The program must already be running")
