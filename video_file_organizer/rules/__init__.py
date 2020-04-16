from video_file_organizer.models import VideoFile

from video_file_organizer.rules import series


def rules_before_matching_vfile(vfile: VideoFile) -> dict:
    if not isinstance(vfile, VideoFile):
        raise TypeError("vfile needs to be an instance of VideoFile")
    if not hasattr(vfile, 'metadata'):
        raise ValueError("vfile needs to have metadata as an attribute")

    name = vfile.name
    metadata = vfile.metadata

    if "alt-title" in vfile.rules:
        metadata = series.rule_alt_title(name, metadata)

    return metadata


def rules_before_transfering_vfile(vfile: VideoFile) -> tuple:
    if not isinstance(vfile, VideoFile):
        raise TypeError("vfile needs to be an instance of VideoFile")
    if not hasattr(vfile, 'metadata'):
        raise ValueError("vfile needs to have metadata as an attribute")
    if not hasattr(vfile, 'foldermatch'):
        raise ValueError("vfile needs to have foldermatch as an attribute")

    name = vfile.name
    metadata = vfile.metadata
    foldermatch = vfile.foldermatch
    rules = vfile.rules
    transfer = vfile.transfer

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

    return transfer, metadata
