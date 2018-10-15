import queue
import os
import logging

from video_file_organizer.obj.file_system_entry \
    import FileSystemEntry
from video_file_organizer.obj.dir_index \
    import DirIndex


def scan_input_dir(app) -> queue.Queue:
    """Returns a Queue with all the FSE"""
    app._requirements(['config'])

    fse_queue: queue.Queue = queue.Queue()

    for item in os.listdir(app.config.input_dir):

        # Ignore config ignore files
        if app.config.ignore:
            if item in app.config.ignore:
                logging.debug("fse '{}' ignored".format(item))
                continue

        fse = FileSystemEntry(app, item)

        # Add FSE to queue is its valid
        if fse.valid:
            logging.debug("fse '{}' added".format(item))
            fse_queue.put(fse)
        else:
            logging.debug("invalid fse {}".format(fse.name))

    return fse_queue


def scan_series_dirs(app) -> DirIndex:
        """Returns a dir_index object for all the series_dirs from the
        configs"""
        app._requirements(['config'])
        return DirIndex(app.config.series_dirs)
