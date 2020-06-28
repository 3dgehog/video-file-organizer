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
from video_file_organizer.rules import RuleCollection, RuleEntry, series

logger = logging.getLogger('vfo.app')


class App:
    def setup(
            self,
            config_dir: Union[str, None] = None,
            create: bool = False
    ) -> None:

        logger.debug("Setting up app")

        self.rule_collection = RuleCollection()
        self.build_rule_collection(self.rule_collection)

        self.configdir = ConfigDirectory(config_dir, create)
        self.config = self.configdir.configfile
        self.rulebook = self.configdir.rulebookfile

        self.transferer = Transferer()

        self.transferer.attach(self.config)

    def run(self, **kwargs) -> None:
        '''
        kwargs:
        whitelist
        '''

        logger.debug("Running app")

        try:
            with yg.lockfile.FileLock(
                    os.path.join(tempfile.gettempdir(), 'vfolock'),
                    timeout=10):

                output_folder = FolderCollection(self.config.series_dirs)
                input_folder = VideoCollection(
                    self.config.input_dir,
                    videoextensions=self.config.videoextensions,
                    whitelist=kwargs.get('whitelist'))

                rule_collection = self.rule_collection

                metadata_matcher = MetadataMatcher()
                rulebook_matcher = RuleBookMatcher(self.rulebook)
                folder_matcher = OutputFolderMatcher(output_folder)

                operations = [
                    metadata_matcher,
                    rulebook_matcher,
                    rule_collection.before_foldermatch,
                    folder_matcher,
                    rule_collection.before_transfer,
                ]

                with input_folder as ifolder:
                    for vfile in ifolder:
                        for operation in operations:
                            operation(vfile=vfile) or \
                                vfile.edit(valid=False)
                        if not vfile.valid:
                            continue

                # Transfer
                with self.transferer as transferer:
                    for vfile in input_folder:
                        transferer.transfer_vfile(vfile)

        except yg.lockfile.FileLockTimeout:
            logger.warning(
                "Lockfile FAILED: The program must already be running")

    def build_rule_collection(self, rule_collection: RuleCollection):
        rule_collection.add_handler(
            RuleEntry('season', series.rule_season, 'before_transfer'))
        rule_collection.add_handler(
            RuleEntry('parent-dir', series.rule_parent_dir, 'before_transfer'))
        rule_collection.add_handler(
            RuleEntry('sub-dir', series.rule_sub_dir, 'before_transfer'))
        rule_collection.add_handler(
            RuleEntry(
                'episode-only',
                series.rule_episode_only,
                'before_transfer')
        )
        rule_collection.add_handler(
            RuleEntry(
                'format-title',
                series.rule_format_title,
                'before_transfer')
        )
        rule_collection.add_handler(
            RuleEntry(
                'alt-title',
                series.rule_alt_title,
                'before_foldermatch')
        )
