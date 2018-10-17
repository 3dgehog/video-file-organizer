import os
import re
import logging
import jinja2

from video_file_organizer.obj.file_system_entry \
    import FileSystemEntry
from video_file_organizer.rules import set_on_event


logger = logging.getLogger('app.series.rules')


def _get_fse(args) -> FileSystemEntry:
    for arg in args:
        if isinstance(arg, FileSystemEntry):
            return arg
    raise ValueError("FileSystemEntry argument wasn't passed")


@set_on_event('after_match')
def rule_season(*args, **kwargs):
    fse = _get_fse(args)
    if 'season' not in fse.rules:
        return
    # Apply Rule
    logger.debug("applying season rule to {}".format(fse.vfile.filename))

    if 'season' not in fse.details:
        logger.warning("FAILED SEASON RULE: ",
                       "Undefined season number from file: ",
                       "{}".format(fse.vfile.filename))
        fse.valid = False
        return

    season = str(fse.details['season'])
    for subdir in fse.matched_dir_entry.subdirs:
        search = re.search("^Season {}".format(season), subdir, re.IGNORECASE)
        if search:
            fse.transfer_to = os.path.join(fse.matched_dir_path, subdir)
            logger.debug("season rule OK {}".format(fse.vfile.filename))

    if not fse.transfer_to:
        logger.warning("FAILED SEASON RULE: " +
                       "Cannot locate season folder: " +
                       "{}".format(fse.vfile.filename))
        fse.valid = False


@set_on_event('after_match')
def rule_parent_dir(*args, **kwargs):
    fse = _get_fse(args)
    if 'parent-dir' not in fse.rules:
        return
    # Apply Rule
    logger.debug("applying parent-dir rule to {}".format(fse.vfile.filename))
    fse.transfer_to = fse.matched_dir_path
    logger.debug("parent-dir rule OK {}".format(fse.vfile.filename))


@set_on_event('after_match')
def rule_sub_dir(*args, **kwargs):
    fse = _get_fse(args)
    if 'sub-dir' not in fse.rules:
        return
    # Apply Rule
    logger.debug("applying sub-dir rule to {}".format(fse.vfile.filename))
    subdir_name_index = fse.rules.index('sub-dir') + 1
    subdir_name = fse.rules[subdir_name_index]
    if subdir_name not in fse.matched_dir_entry.subdirs:
        logger.warning("FAILED SUB-DIR RULE: " +
                       "Cannot locate sub-dir {}: ".format(subdir_name) +
                       "{}".format(fse.vfile.filename))
        fse.valid = False
        return

    fse.transfer_to = os.path.join(fse.matched_dir_path, subdir_name)
    logger.debug("sub-dir rule OK {}".format(fse.vfile.filename))


@set_on_event('after_match', order=9)
def rule_episode_only(*args, **kwargs):
    fse = _get_fse(args)
    if 'episode-only' not in fse.rules:
        return
    # Apply Rule
    logger.debug("applying episode-only rule to {}".format(fse.vfile.filename))
    try:
        fse.details['episode'] = int(
            str(fse.details['season']) + str(fse.details['episode']))
    except KeyError:
        # Any episode number below 100 will raise... therefore its ignored
        pass
    fse.details.pop('season', None)
    logger.debug("episode-only rule OK {}".format(fse.vfile.filename))


@set_on_event('before_transfer')
def rule_format_title(*args, **kwargs):
    fse = _get_fse(args)
    if 'format-title' not in fse.rules:
        return
    # Apply Rule
    if not fse.details.get('container') or not fse.transfer_to:
        logger.warning("FAILED FORMAT-TITLE RULE: " +
                       "Missing container or transfer_to value: " +
                       "{}".format(fse.vfile.filename))
        fse.valid = False
        return

    format_index = fse.rules.index('format-title') + 1
    template = jinja2.Template(
        str(fse.rules[format_index]) + "." + str(fse.details['container']))
    new_name = template.render(fse.details)
    fse.transfer_to = os.path.join(fse.transfer_to, new_name)
    logger.debug("format-title rule OK {}".format(fse.vfile.filename))
