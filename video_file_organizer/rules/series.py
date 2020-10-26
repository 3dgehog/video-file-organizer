import os
import re
import logging
import jinja2

from video_file_organizer.entries import VideoFileEntry

logger = logging.getLogger('vfo.rules.series')


def rule_season(vfile: VideoFileEntry):
    if 'season' not in vfile.metadata:
        return vfile.error(f"Undefined season number for file: {vfile.name}")

    season = str(vfile.metadata['season'])
    for entry in vfile.foldermatch:
        search = re.search(f"^Season {season}", entry.name, re.IGNORECASE)
        if search:
            vfile.update(transfer=entry.path)

    if not vfile.transfer:
        path_to_new_season_dir = os.path.join(
            vfile.foldermatch.path, f"Season {season}")
        os.mkdir(path_to_new_season_dir)
        vfile.update(transfer=path_to_new_season_dir)
        logger.info("RULE 'season' Created new Season " +
                    f"{season} folder for Series {vfile.name}")


def rule_parent_dir(vfile: VideoFileEntry):
    vfile.update(transfer=vfile.foldermatch.path)


def rule_sub_dir(vfile: VideoFileEntry):
    subdir_name_index = vfile.rules.index('sub-dir') + 1
    subdir_name = vfile.rules[subdir_name_index]

    if subdir_name not in vfile.foldermatch.list_entries_by_name():
        return vfile.error(
            f"Cannot locate sub-dir {subdir_name}: {vfile.name}")

    vfile.update(
        transfer=vfile.foldermatch.get_entry_by_name(subdir_name).path)


def rule_episode_only(vfile: VideoFileEntry):
    metadata = vfile.metadata.copy()
    try:
        metadata['episode'] = int(
            str(vfile.metadata['season']) + str(vfile.metadata['episode']))
    except KeyError:
        # Any episode number below 100 will raise... therefore its ignored
        pass

    vfile.update(metadata=metadata, merge=False)


def rule_format_title(vfile: VideoFileEntry):

    if 'container' not in vfile.metadata:
        return vfile.error(
            f"Missing 'container' in metadata for: {vfile.name}")

    if not vfile.transfer:
        return vfile.error(f"Missing 'transfer' value for: {vfile.name}")

    format_index = vfile.rules.index('format-title') + 1

    template = jinja2.Template(
        str(vfile.rules[format_index]) + "." + str(vfile.metadata['container'])
    )
    new_name = template.render(vfile.metadata)

    vfile.update(
        transfer=os.path.join(vfile.transfer, new_name))


def rule_alt_title(vfile: VideoFileEntry):
    if 'alternative_title' not in vfile.metadata:
        return vfile.error(f"Alternative title missing: {vfile.name}")

    metadata = vfile.metadata.copy()

    metadata['title'] = ' '.join([
        vfile.metadata['title'], vfile.metadata['alternative_title']
    ])

    vfile.update(metadata=metadata, merge=False)
