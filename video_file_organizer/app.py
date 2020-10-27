import logging
import sys
from typing import List, Callable
from filelock import Timeout, FileLock

from video_file_organizer.config import Config, RuleBook
from video_file_organizer.transferer import Transferer
from video_file_organizer.entries import InputDirectory, OutputDirectories
from video_file_organizer.matchers import GuessItMatcher, \
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

                output_folder = OutputDirectories(self.config.series_dirs)

                operations: List[Callable] = [
                    GuessItMatcher(),
                    RuleBookMatcher(self.rulebook),
                    OutputFolderMatcher(output_folder)
                ]

                # Attach Observers to operations
                for operation in operations:
                    operation.register_multiple_observers(
                        [self.config, self.rulebook.rulebook_registry])

                for vfile in input_folder.videofilelist:
                    for operation in operations:
                        with operation:

                            operation.notify_observers(
                                topic=f'{operation.__class__.__name__}/before',
                                vfile=vfile)

                            operation(vfile)

                            operation.notify_observers(
                                topic=f'{operation.__class__.__name__}/after',
                                vfile=vfile)

                transferer = Transferer()
                transferer.register_multiple_observers(
                    [self.config, self.rulebook.rulebook_registry])

                with transferer:
                    for vfile in input_folder.videofilelist:
                        if not vfile.valid:
                            continue

                        transferer.notify_observers(
                            topic=f'{operation.__class__.__name__}/before',
                            vfile=vfile)

                        transferer(vfile)

                        transferer.notify_observers(
                            topic=f'{operation.__class__.__name__}/after',
                            vfile=vfile)

        except Timeout:
            logger.warning(
                "Another instance of this app currently holds the lock.")
            sys.exit(1)
