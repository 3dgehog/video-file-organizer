import os
import re
import logging
import guessit
import jinja2
import glob

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
    """Sets transfer_to to the correct season folder based on the fse
    filename"""
    fse = _get_fse(args)
    if 'season' not in fse.rules:
        return
    # Apply Rule
    logger.debug("applying season rule to {}".format(fse.vfile.filename))

    if 'season' not in fse.details:
        logger.log(11, "FAILED SEASON RULE: ",
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
        logger.log(11, "FAILED SEASON RULE: " +
                   "Cannot locate season folder: " +
                   "{}".format(fse.vfile.filename))
        fse.valid = False


@set_on_event('after_match')
def rule_parent_dir(*args, **kwargs):
    """Sets transfer_to to the parent directory"""
    fse = _get_fse(args)
    if 'parent-dir' not in fse.rules:
        return
    # Apply Rule
    logger.debug("applying parent-dir rule to {}".format(fse.vfile.filename))
    fse.transfer_to = fse.matched_dir_path
    logger.debug("parent-dir rule OK {}".format(fse.vfile.filename))


@set_on_event('after_match')
def rule_sub_dir(*args, **kwargs):
    """Sets the transfer_to a specified sub directory"""
    fse = _get_fse(args)
    if 'sub-dir' not in fse.rules:
        return
    # Apply Rule
    logger.debug("applying sub-dir rule to {}".format(fse.vfile.filename))
    subdir_name_index = fse.rules.index('sub-dir') + 1
    subdir_name = fse.rules[subdir_name_index]
    if subdir_name not in fse.matched_dir_entry.subdirs:
        logger.log(11, "FAILED SUB-DIR RULE: " +
                   "Cannot locate sub-dir {}: ".format(subdir_name) +
                   "{}".format(fse.vfile.filename))
        fse.valid = False
        return

    fse.transfer_to = os.path.join(fse.matched_dir_path, subdir_name)
    logger.debug("sub-dir rule OK {}".format(fse.vfile.filename))


@set_on_event('after_match', order=9)
def rule_episode_only(*args, **kwargs):
    """Removes fse.detail['season'] and merges it with fse.detail['episode']"""
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
    """Sets transfer_to filename to a specified name for transfer"""
    fse = _get_fse(args)
    if 'format-title' not in fse.rules:
        return
    # Apply Rule
    if not fse.details.get('container') or not fse.transfer_to:
        logger.log(11, "FAILED FORMAT-TITLE RULE: " +
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


@set_on_event('before_match')
def rule_alt_title(*args, **kwargs):
    """Checks if the fse has an alternative title and merges it with the
    current title"""
    fse = _get_fse(args)
    if 'alt-title' not in fse.rules:
        return
    # Apply Rule
    if 'alternative_title' not in fse.details:
        logger.log(11, "FAILED ALT-TITLE RULE: " +
                   "Alternative title missing: " +
                   "{}".format(fse.vfile.filename))
        fse.valid = False
        return
    fse.title = ' '.join([
        fse.details['title'], fse.details['alternative_title']
    ])
    logger.debug("alt-title rule OK {}".format(fse.vfile.filename))


@set_on_event('before_transfer')
def rule_no_replace(*args, **kwargs):
    """This rule first detects if a duplicate episode is found.
    If found, it will determine to replace it or not based on if
    the episode is proper or not. It will also just ignore replacing
    it if the rule no-replace was set for this series"""
    fse = _get_fse(args)
    # Apply Rule
    # Get directory of transfer for fse
    if not os.path.isdir(fse.transfer_to):
        transfer_to = os.path.dirname(fse.transfer_to)
    else:
        transfer_to = fse.transfer_to

    # Global search all files for same episode number
    glob_search = glob.glob(
        "{}/*{}*".format(transfer_to, fse.details['episode']))
    if len(glob_search) == 0:
        logger.debug("REPLACE: no duplicate episode")
        if 'no-replace' in fse.rules:
            logger.debug("no-replace rule OK {}".format(fse.vfile.filename))
        return

    # Iterate thru global search
    for item in glob_search:
        item_detail = guessit.guessit(item)
        try:
            if item_detail['episode'] != fse.details['episode']:
                continue
        except KeyError:
            continue
        logger.debug(
            "REPLACE: same episode found: new -> {}: existing -> {}".format(
                fse.vfile.filename, os.path.basename(item))
        )

        # Prevent episode being replaced
        if 'no-replace' in fse.rules:
            logger.debug("no-replace rule OK {}".format(fse.vfile.filename))
            fse.transfer_to = None
            # NOTE: Probably need to find a way to remove this episode
            return

        # Check if any of the 2 episodes are proper's
        cur = False
        ext = False
        if 'proper_count' in fse.details:
            cur = True
        if 'proper_count' in item_detail:
            ext = True

        if cur and ext:
            logger.log(11, "REPLACE: both are proper, favoring the new")
            fse.replace = os.path.join(transfer_to, item)

        elif cur and not ext:
            logger.log(11,
                       "REPLACE: this file proper, existing isn't, replacing")
            fse.replace = os.path.join(transfer_to, item)

        elif ext and not cur:
            logger.log(11,
                       "REPLACE: this file isn't proper, existing is, ",
                       "not replacing")
            fse.transfer_to = None

        else:
            logger.log(11, "REPLACE: both are normal, favoring the new")
            fse.replace = os.path.join(fse.transfer_to, item)
        break
