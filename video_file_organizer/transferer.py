import logging
import shutil
import os

from video_file_organizer.obj.file_system_entry import FileSystemEntry

logger = logging.getLogger('app.transferer')


def transferer(app):
    app._requirements(['matched_queue', 'event'])
    logger.debug("Running Transferer")

    matched_queue = app.matched_queue

    while True:
        if matched_queue.qsize() == 0:
            logger.debug("end of matched queue")
            break

        fse = matched_queue.get()

        logger.debug("working on {}".format(fse.vfile.filename))

        transfer_fse(app, fse)


def transfer_fse(app, fse: FileSystemEntry):
    app.event.before_transfer(fse)
    _transfer_fse(app, fse)
    app.event.after_transfer(fse)


def _transfer_fse(app, fse: FileSystemEntry):
    if not fse.valid or not fse.transfer_to:
        return
    _copy_fse(fse)
    _delete_fse(fse)


def _copy_fse(fse: FileSystemEntry):
    logger.debug("copying: '{}' to: '{}'".format(
        fse.vfile.filename, fse.transfer_to))
    shutil.copy(fse.vfile.abspath, fse.transfer_to)


def _delete_fse(fse: FileSystemEntry):
    if fse.isdir:
        shutil.rmtree(fse.abspath)
    else:
        os.remove(fse.abspath)
    logger.debug("fse deleted")
