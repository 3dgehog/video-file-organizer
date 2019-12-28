import queue
import os
import logging
import guessit

from video_file_organizer.models import FileSystemEntry, DirIndex


logger = logging.getLogger('app.scanner')


def scan_input_dir(config, rule_book) -> queue.Queue:
    """Returns a Queue with all the FSE"""
    logger.debug("Scanning input dir")

    scan_queue = queue.Queue()

    for item in os.listdir(config.input_dir):

        # Ignore config ignore files
        if config.ignore:
            if item in config.ignore:
                logger.debug("FSE '{}' ignored".format(item))
                continue

        logger.debug("Scanning {}".format(item))

        fse = FileSystemEntry(config.input_dir, item)
        _scan_fse_files(fse, config.re_file_ext_pattern)
        if fse.vfile.filename is not None:
            _scan_fse_details(fse)
            fse.rules = rule_book.get_fse_rules(fse)
            logger.debug("FSE '{}' added to scan_queue".format(item))
            scan_queue.put(fse)
        else:
            logger.debug("Invalid FSE {}".format(fse.name))

    return scan_queue


def scan_series_dirs(config) -> DirIndex:
    """
    Returns a dir_index object for all the series_dirs from the
    configs
    """
    logger.debug("Scanning series dirs")
    return DirIndex(config.series_dirs)


###

def _scan_fse_files(fse, re_file_ext_pattern):
    """Scans FSE and validates it. If its a valid object, self.valid will
    be set to true"""
    if fse.isdir:
        for item in os.listdir(fse.abspath):
            # if secondary directory, ignore
            if os.path.isdir(os.path.join(fse.abspath, item)):
                continue

            # if file has file extension
            if re_file_ext_pattern.match(item):
                # if file was already valid, break and set to not valid
                # reason: does not support multiple files right now!!
                if fse.vfile.filename:
                    logger.debug(
                        "More than one video file ",
                        "found, invalid fse {}".format(fse.name))
                    fse.valid = False
                    break
                fse.vfile.filename = item
                fse.vfile.abspath = os.path.join(fse.abspath, item)

    else:
        # check if the file found has a valid file extension
        if re_file_ext_pattern.match(fse.name):
            fse.vfile.filename = fse.name
            fse.vfile.abspath = fse.abspath


def _scan_fse_details(fse):
    """Scans the FSE filename and foldername to guess all the details
    about it. """
    guessitmatch = guessit.guessit(fse.vfile.filename)

    if fse.isdir:
        # Guess the dir name
        guessitmatch_foldername = guessit.guessit(fse.name)
        # keep the better guess from the filename or the foldername
        if len(guessitmatch_foldername) > len(guessitmatch):
            guessitmatch = guessitmatch_foldername
            logger.debug(
                "Used foldername instead of filename for guessit match.")
    fse.details = guessitmatch

    # Try to set the title from the guessitmatch
    if 'title' not in guessitmatch:
        logger.log(11, "NO TITLE MATCH: ",
                   "Unable to find title for: ",
                   "{}".format(fse.vfile.filename))
        fse.valid = False

    if 'type' not in guessitmatch:
        logger.log(11, "NO TYPE MATCH: ",
                   "Unable to find type of video for: ",
                   "{}".format(fse.vfile.filename))
        fse.valid = False

    try:
        fse.title = guessitmatch['title']
        fse.type = guessitmatch['type']
    except KeyError:
        pass
