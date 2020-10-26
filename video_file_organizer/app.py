import logging
import sys
from typing import List, Callable
from filelock import Timeout, FileLock

from video_file_organizer.config import Config, RuleBook
from video_file_organizer.transferer import Transferer
from video_file_organizer.entries import InputDirectory, OutputDirectories
from video_file_organizer.matchers import MetadataMatcher, \
    RuleBookMatcher, OutputFolderMatcher

logger = logging.getLogger('vfo.app')


class App:
    def setup(self, args=None) -> None:

        logger.debug("Setting up app")

        self.config = Config(args)
        self.rulebook = RuleBook(args)

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

                # Attach Observee's to Observers
                for operation in operations:
                    operation.attach_multiple(
                        [self.config, self.rulebook.rulebook_registry])

                # Run each operation with vfiles
                for vfile in input_folder.videofilelist:
                    for operation in operations:
                        if not vfile.valid:
                            break
                        operation.notify(
                            topic=f'{operation.__class__.__name__}/before',
                            vfile=vfile)
                        operation(vfile)
                        operation.notify(
                            topic=f'{operation.__class__.__name__}/after',
                            vfile=vfile)

                # Detach Observee's to Observers
                for operation in operations:
                    operation.detach_all()

                # Remove vfile that are not valid
                invalid_vfile = [vfile for vfile in input_folder.videofilelist
                                 if not vfile.valid]
                for vfile in invalid_vfile:
                    input_folder.videofilelist.remove(vfile)

                # Run Transfer
                with Transferer() as transferer:
                    transferer.attach_multiple(
                        [self.config, self.rulebook.rulebook_registry])
                    for vfile in input_folder.videofilelist:
                        transferer.transfer_vfile(vfile)
                    transferer.detach_all()

        except Timeout:
            logger.warning(
                "Another instance of this app currently holds the lock.")
            sys.exit(1)
