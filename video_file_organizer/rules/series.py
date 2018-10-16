import os
import re
import logging

from video_file_organizer.obj.file_system_entry \
    import FileSystemEntry
from video_file_organizer.rules import set_on_event


logger = logging.getLogger('app.series.rules')


def _get_fse(args) -> FileSystemEntry:
    for arg in args:
        if isinstance(arg, FileSystemEntry):
            return arg
    raise ValueError("FileSystemEntry argument wasn't passed")


@set_on_event('before_transfer')
def rule_season(*args, **kwargs):
    fse = _get_fse(args)
    if 'season' not in fse.rules:
        return
    # Apply Rule
    if 'season' not in fse.details:
        logger.warning("NO DETAIL 'season':{}".format(
                fse.vfile.filename))
        fse.valid = False
        return

    season = str(fse.details['season'])
    for subdir in fse.matched_dir_entry.subdirs:
        search = re.search("^Season {}".format(season), subdir, re.IGNORECASE)
        if search:
            fse.transfer_to = os.path.join(fse.matched_dir_path, subdir)

    if not fse.transfer_to:
        logger.warning("NO SEASON FOLDER:{}".format(fse.vfile.filename))
        fse.valid = False


@set_on_event('before_transfer')
def rule_parent_dir(*args, **kwargs):
    fse = _get_fse(args)
    if 'parent-dir' not in fse.rules:
        return
    # Apply Rule
    fse.transfer_to = fse.matched_dir_path


@set_on_event('before_transfer')
def rule_sub_dir(*args, **kwargs):
    fse = _get_fse(args)
    if 'sub-dir' not in fse.rules:
        return
    # Apply Rule
    subdir_name_index = fse.rules.index('sub-dir') + 1
    subdir_name = fse.rules[subdir_name_index]
    if subdir_name not in fse.matched_dir_entry.subdirs:
        logger.warning("NO SUBDIR '{}':{}".format(
            subdir_name, fse.vfile.filename))
        fse.valid = False
        return

    fse.transfer_to = os.path.join(fse.matched_dir_path, subdir_name)
