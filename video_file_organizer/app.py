import logging
import sys
from typing import List, Callable
from filelock import Timeout, FileLock

from video_file_organizer.config import Config, RuleBook
from video_file_organizer.transferer import Transferer
from video_file_organizer.utils import Observee
from video_file_organizer.entries import InputDirectory, OutputDirectories
from video_file_organizer.matchers import MetadataMatcher, \
    RuleBookMatcher, OutputFolderMatcher
from video_file_organizer.utils import vfile_consumer

logger = logging.getLogger('vfo.app')


class App:
    def setup(self, args=None) -> None:

        logger.debug("Setting up app")

        self.config = Config(args)
        self.rulebook = RuleBook(args)

        Observee.attach(self.rulebook.rulebook_registry)
        Observee.attach(self.config)

        self.lock = FileLock('.vfo.lock', timeout=60)

    def run(self, **kwargs):
        logger.debug("Running app")
        try:
            with self.lock:

                input_folder = InputDirectory(
                    self.config.input_dir,
                    videoextensions=self.config.videoextensions,
                    whitelist=kwargs.get('whitelist'))
                input_folder.entries
                output_folder = OutputDirectories(self.config.series_dirs)

                operations: List[Callable] = [
                    MetadataMatcher(),
                    RuleBookMatcher(self.rulebook),
                    OutputFolderMatcher(output_folder)
                ]

                for vfile in input_folder.videofilelist:
                    for operation in operations:
                        if not vfile.valid:
                            break
                        vfile_consumer(operation.__class__.__name__)(
                            operation)(vfile=vfile)

                invalid_vfile = [vfile for vfile in input_folder.videofilelist
                                 if not vfile.valid]
                for vfile in invalid_vfile:
                    input_folder.videofilelist.remove(vfile)

                with Transferer() as transferer:
                    for vfile in input_folder.videofilelist:
                        transferer.transfer_vfile(vfile)

        except Timeout:
            logger.warning(
                "Another instance of this app currently holds the lock.")
            sys.exit(1)
