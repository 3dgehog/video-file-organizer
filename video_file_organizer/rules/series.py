import os
import re
import logging

from video_file_organizer.obj.file_system_entry \
    import FileSystemEntry
from video_file_organizer.rules import set_on_event


logger = logging.getLogger('rules.series')


@set_on_event('before_transfer')
def rule_season(fse: FileSystemEntry, *args, **kwargs):
    if not isinstance(fse, FileSystemEntry):
        raise ValueError("Received an argument other than a FileSystemEntry")
    if 'season' not in fse.rules:
        return
    # Apply Rule
    if 'season' not in fse.details:
        logger.warning(
            "Couldn't find 'season' from details of {}".format(
                fse.vfile.filename))
        fse.valid = False
    season = str(fse.details['season'])
    for subdir in fse.matched_dir_entry.subdirs:
        search = re.search("^Season {}".format(season), subdir, re.IGNORECASE)
        if search:
            fse.transfer_to = os.path.join(fse.matched_dir_path, subdir)
    if not fse.transfer_to:
        logger.warning("Couldn't find Season subdir")
        fse.valid = False


@set_on_event('before_transfer')
def rule_parent_dir(fse: FileSystemEntry, *args, **kwargs):
    if not isinstance(fse, FileSystemEntry):
        raise ValueError("Received an argument other than a FileSystemEntry")
    if 'parent-dir' not in fse.rules:
        return
    # Apply Rule
    fse.transfer_to = fse.matched_dirpath


@set_on_event('before_transfer')
def rule_sub_dir(fse: FileSystemEntry, *args, **kwargs):
    if not isinstance(fse, FileSystemEntry):
        raise ValueError("Received an argument other than a FileSystemEntry")
    if 'sub-dir' not in fse.rules:
        return
    # Apply Rule
    subdir_name_index = fse.rules.index('subdir') + 1
    subdir_name = fse.rules[subdir_name_index]
    if subdir_name not in fse.matched_dir_entry.subdirs:
        logger.warning("Couldn't find subdir {}".format(subdir_name))
        fse.valid = False
    else:
        fse.transfer_to = os.path.join(fse.matched_dirpath, subdir_name)
