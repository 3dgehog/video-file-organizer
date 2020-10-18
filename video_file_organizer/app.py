import logging
import sys
from typing import List, Callable
from filelock import Timeout, FileLock

from video_file_organizer.config import Config, RuleBook
from video_file_organizer.models import VideoCollection, FolderCollection
from video_file_organizer.matchers import OutputFolderMatcher, \
    RuleBookMatcher, MetadataMatcher
from video_file_organizer.transferer import Transferer
from video_file_organizer.utils import Observee, vfile_consumer

logger = logging.getLogger('vfo.app')


class App:
    def setup(self, args=None) -> None:

        logger.debug("Setting up app")

        self.config = Config(args)
        self.rulebook = RuleBook(args)

        Observee.attach(self.rulebook.rulebook_registry)
        Observee.attach(self.config)

        self.lock = FileLock('.vfo.lock', timeout=60)

    def run(self, **kwargs) -> None:
        logger.debug("Running app")

        try:
            with self.lock:
                output_folder = FolderCollection(self.config.series_dirs)
                input_folder = VideoCollection(
                    self.config.input_dir,
                    videoextensions=self.config.videoextensions,
                    whitelist=kwargs.get('whitelist'))

                operations: List[Callable] = [
                    MetadataMatcher(),
                    RuleBookMatcher(self.rulebook),
                    OutputFolderMatcher(output_folder),
                ]

                # Gathering data
                with input_folder as ifolder:
                    for vfile in ifolder:
                        for operation in operations:
                            if not vfile.valid:
                                break
                            vfile_consumer(operation.__class__.__name__)(
                                operation)(vfile=vfile)

                # Transfering
                with Transferer() as transferer:
                    for vfile in input_folder:
                        transferer.transfer_vfile(vfile)
        except Timeout:
            logger.warning(
                "Another instance of this app currently holds the lock.")
            sys.exit(1)
