import os
import logging
import tempfile
import yg.lockfile

from video_file_organizer.config import Config, RuleBook
from video_file_organizer.models import VideoCollection, FolderCollection
from video_file_organizer.rules.utils import RuleRegistry
from video_file_organizer.matchers import OutputFolderMatcher, \
    RuleBookMatcher, MetadataMatcher
from video_file_organizer.transferer import Transferer
from video_file_organizer.utils import Observee

logger = logging.getLogger('vfo.app')


class App:
    def setup(self, args=None) -> None:

        logger.debug("Setting up app")

        self.config = Config(args)
        self.rulebook = RuleBook(args)

        self.rule_registry = RuleRegistry()

        Observee.attach(self.rule_registry)
        Observee.attach(self.config)

    def run(self, **kwargs) -> None:
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

                operations = [
                    MetadataMatcher(),
                    RuleBookMatcher(self.rulebook),
                    OutputFolderMatcher(output_folder),
                ]

                with input_folder as ifolder:
                    for vfile in ifolder:
                        for operation in operations:
                            operation(vfile=vfile)
                        if not vfile.valid:
                            continue

                # Transfer
                with Transferer() as transferer:
                    for vfile in input_folder:
                        transferer.transfer_vfile(vfile)

        except yg.lockfile.FileLockTimeout:
            logger.info(
                "Lockfile FAILED: The program must already be running")
