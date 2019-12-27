import queue
import os
import logging

from video_file_organizer.obj.file_system_entry \
    import FileSystemEntry
from video_file_organizer.obj.dir_index \
    import DirIndex


logger = logging.getLogger('app.scanner')


def scan_input_dir(app) -> queue.Queue:
    """Returns a Queue with all the FSE"""
    logger.debug("Scanning input dir")

    scan_queue = queue.Queue()

    for item in os.listdir(app.config.input_dir):

        # Ignore config ignore files
        if app.config.ignore:
            if item in app.config.ignore:
                logger.debug("FSE '{}' ignored".format(item))
                continue

        logger.debug("Scanning {}".format(item))
        fse = FileSystemEntry(app, item)

        # Add FSE to queue is its valid
        if fse.valid:
            logger.debug("FSE '{}' added to scan_queue".format(item))
            scan_queue.put(fse)
        else:
            logger.debug("Invalid FSE {}".format(fse.name))

    return scan_queue


def scan_series_dirs(app) -> DirIndex:
    """
    Returns a dir_index object for all the series_dirs from the
    configs
    """
    logger.debug("Scanning series dirs")
    return DirIndex(app.config.series_dirs)
