import logging
import sys
import os

from typing import List, Callable
from filelock import Timeout, FileLock

from .config import Config, RuleBook
from .transferer import Transferer
from .entries import InputDirectory, OutputDirectories
from .matchers import GuessItMatcher, RuleBookMatcher, OutputFolderMatcher
from .database import Database

logger = logging.getLogger('vfo.app')


class App:
    def setup(self, args=None) -> None:

        logger.debug("Setting up app")

        self.config = Config(args)
        self.rulebook = RuleBook(args)

        self.lock = FileLock(
            os.path.join(self.config.input_dir, '.vfo.lock'),
            timeout=60)

        self.database = Database()

    def run(self, **kwargs):
        logger.debug("Running app")
        try:
            with self.lock:

                input_folder = InputDirectory(
                    self.config.input_dir,
                    videoextensions=self.config.videoextensions,
                    whitelist=kwargs.get('whitelist'),
                    database=self.database)

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

                transferer = Transferer(self.database)
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
