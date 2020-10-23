import os
import re
import logging
import jinja2

from video_file_organizer.entries import VideoFileEntry

logger = logging.getLogger('vfo.series.rules')


def rule_season(vfile: VideoFileEntry):
    """Sets transfer to the correct season folder"""
    logger.debug(f"RULE 'season' to {vfile.name}")

    if 'season' not in vfile.metadata:
        vfile.error(f"Undefined season number for file: {vfile.name}")
        return

    season = str(vfile.metadata['season'])
    for entry in vfile.foldermatch:
        search = re.search(f"^Season {season}", entry.name, re.IGNORECASE)
        if search:
            vfile.transfer = entry.path

    if not vfile.transfer:
        path_to_new_season_dir = os.path.join(
            vfile.foldermatch.path, f"Season {season}")
        os.mkdir(path_to_new_season_dir)
        vfile.transfer = path_to_new_season_dir
        logger.info("Rule 'season' Created new Season " +
                    f"{season} folder for Series {vfile.name}")

    logger.debug(f"RULE 'season' OK for {vfile.name}")


def rule_parent_dir(vfile: VideoFileEntry):
    """Sets 'transfer to the parent directory"""
    logger.debug(f"Applying rule 'parent-dir' to {vfile.name}")
    vfile.transfer = vfile.foldermatch.path

    logger.debug(f"Rule 'parent-dir' OK for {vfile.name}")
    return


def rule_sub_dir(vfile: VideoFileEntry):
    """Sets the transfer a specified sub directory"""
    logger.debug(f"Applying rule 'sub-dir' to {vfile.name}")

    subdir_name_index = vfile.rules.index('sub-dir') + 1
    subdir_name = vfile.rules[subdir_name_index]

    if subdir_name not in vfile.foldermatch.list_entries_by_name():
        vfile.error(f"Cannot locate sub-dir {subdir_name}: {vfile.name}")
        return

    vfile.transfer = vfile.foldermatch.get_entry_by_name(
        subdir_name).path

    logger.debug(f"Rule 'sub-dir' OK for {vfile.name}")
    return


def rule_episode_only(vfile: VideoFileEntry):
    """Removes guessit['season'] and merges it with guessit['episode']"""
    logger.debug(f"Applying rule 'episode-only' to {vfile.name}")
    try:
        vfile.metadata['episode'] = int(
            str(vfile.metadata['season']) + str(vfile.metadata['episode']))
    except KeyError:
        # Any episode number below 100 will raise... therefore its ignored
        pass

    logger.debug(f"Rule 'episode-only' OK for {vfile.name}")
    return


def rule_format_title(vfile: VideoFileEntry):
    """Sets transfer filename to a specified name for transfer"""
    logger.debug(f"Applying rule 'format-title' to {vfile.name}")

    if not vfile.metadata.get('container') \
            or not vfile.transfer:
        vfile.error(f"Missing container or transfer value: {vfile.name}")

    format_index = vfile.rules.index('format-title') + 1
    template = jinja2.Template(
        str(vfile.rules[format_index]) + "." + str(vfile.metadata['container'])
    )
    new_name = template.render(vfile.metadata)
    vfile.transfer = os.path.join(
        vfile.transfer, new_name)

    logger.debug(f"Rule 'format-title' OK for {vfile.name}")
    return


def rule_alt_title(vfile: VideoFileEntry):
    """Checks if the fse has an alternative title and merges it with the
    current title"""
    logger.debug(f"Applying rule 'alternative_title' to {vfile.name}")

    if 'alternative_title' not in vfile.metadata:
        vfile.error(f"Alternative title missing: {vfile.name}")
        return

    vfile.metadata['title'] = ' '.join([
        vfile.metadata['title'], vfile.metadata['alternative_title']
    ])

    logger.debug(f"Rule 'alternative_title' OK for {vfile.name}")
    return
