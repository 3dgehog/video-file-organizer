import queue
import logging
import difflib

from video_file_organizer.obj.file_system_entry \
    import FileSystemEntry


logger = logging.getLogger('app.matcher')


def matcher(app) -> queue.Queue:
    app._requirements(['scan_queue', 'event', 'series_index'])

    logger.debug("Running Matcher")
    match_queue = queue.Queue()

    scan_queue = app.scan_queue

    while True:
        # scan_queue is empty, break
        if scan_queue.qsize() == 0:
            logger.debug("End of scan queue")
            break

        # Get FSE object from scan_queue
        fse = scan_queue.get()

        match_fse(app, fse)
        if not fse.valid or not fse.transfer_to:
            continue

        logger.debug("Added {} to match queue".format(fse.vfile.filename))
        match_queue.put(fse)

    return match_queue


def match_fse(app, fse: FileSystemEntry):
    app.event.before_match(fse)
    _match_fse(app, fse)
    if fse.valid:
        app.event.after_match(fse)


def _match_fse(app, fse: FileSystemEntry):
    INDEX = {
        'episode': app.series_index
    }
    index = INDEX.get(fse.type)
    if not index:
        logger.log(11, "FAILED INDEX: " +
                   "Unable to find index for type {}: ".format(fse.type) +
                   "{}".format(fse.vfile.filename))
        fse.valid = False
        return

    index_match = difflib.get_close_matches(
        fse.title, index.keys, n=1, cutoff=0.6)

    if not index_match:
        logger.log(11, "FAILED MATCH: " +
                   "Unable to find a match: " +
                   "{}".format(fse.vfile.filename))
        fse.valid = False
        return

    fse.matched_dir_path = index.dict[index_match[0]].path
    fse.matched_dir_name = index_match[0]
    fse.matched_dir_entry = index.dict[index_match[0]]
    logger.debug("Match successful for {}".format(fse.vfile.filename))
