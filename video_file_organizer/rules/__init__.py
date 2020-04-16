from video_file_organizer.models import VideoFile

from video_file_organizer.rules import series
from video_file_organizer.utils import vfile_options


@vfile_options('name', 'metadata')
def rules_before_matching_vfile(vfile: VideoFile, **kwargs) -> dict:
    name = kwargs['name']
    metadata = kwargs['metadata']

    if "alt-title" in vfile.rules:
        metadata = series.rule_alt_title(name, metadata)

    return {'metadata': metadata}


@vfile_options('name', 'metadata', 'foldermatch', 'rules', 'transfer')
def rules_before_transfering_vfile(vfile: VideoFile, **kwargs) -> dict:

    name = kwargs['name']
    metadata = kwargs['metadata']
    foldermatch = kwargs['foldermatch']
    rules = kwargs['rules']
    transfer = kwargs['transfer']

    if "season" in rules:
        transfer.update(series.rule_season(name, metadata, foldermatch))

    if "parent-dir" in rules:
        transfer.update(series.rule_parent_dir(name, foldermatch))

    if "sub-dir" in rules:
        transfer.update(series.rule_sub_dir(name, foldermatch, rules))

    if "episode-only" in rules:
        metadata.update(series.rule_episode_only(name, metadata))

    if "format-title" in rules:
        transfer.update(series.rule_format_title(
            name, metadata, rules, transfer))

    return {'transfer': transfer, 'metadata': metadata}
