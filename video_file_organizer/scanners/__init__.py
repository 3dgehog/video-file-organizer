import queue
import os
import logging

from video_file_organizer.scanners.file_system_entry \
    import FileSystemEntry
from video_file_organizer.scanners.series_dirs_index \
    import SeriesDirsIndex
from video_file_organizer.configs.config_handler \
    import ConfigHandler


def scan_input_dir(config: ConfigHandler) -> queue.Queue:
    """Returns a Queue with all the FSE"""

    fse_queue: queue.Queue = queue.Queue()

    for item in os.listdir(config.input_dir):

        # Ignore config ignore files
        if config.ignore:
            if item in config.ignore:
                logging.debug("fse '{}' ignored".format(item))
                continue

        fse = FileSystemEntry(config, item)

        # Add FSE to queue is its valid
        if fse.valid:
            logging.debug("fse '{}' added".format(item))
            fse_queue.put(fse)
        else:
            logging.debug("invalid fse {}".format(fse.name))

    return fse_queue


def scan_series_dirs(config: ConfigHandler) -> SeriesDirsIndex:
    """Returns a series_dirs_index object"""
    return SeriesDirsIndex(config)
