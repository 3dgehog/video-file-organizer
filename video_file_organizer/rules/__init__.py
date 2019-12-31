from video_file_organizer.models import VideoFile

from video_file_organizer.rules import series


def rules_before_matching_vfile(vfile: VideoFile) -> dict:
    if not isinstance(vfile, VideoFile):
        raise TypeError("vfile needs to be an instance of VideoFile")
    if not hasattr(vfile, 'guessit'):
        raise ValueError("vfile needs to have guessit as an attribute")

    name = vfile.name
    guessit = vfile.guessit

    if "alt-title" in vfile.rules:
        guessit = series.rule_alt_title(name, guessit)

    return guessit


def rules_before_transfering_vfile(vfile: VideoFile) -> tuple:
    if not isinstance(vfile, VideoFile):
        raise TypeError("vfile needs to be an instance of VideoFile")
    if not hasattr(vfile, 'guessit'):
        raise ValueError("vfile needs to have guessit as an attribute")
    if not hasattr(vfile, 'match'):
        raise ValueError("vfile needs to have match as an attribute")
    if not hasattr(vfile, 'transfer'):
        vfile.transfer = {}

    name = vfile.name
    guessit = vfile.guessit
    match = vfile.match
    rules = vfile.rules
    transfer = vfile.transfer

    if "season" in rules:
        transfer.update(series.rule_season(name, guessit, match))

    if "parent-dir" in rules:
        transfer.update(series.rule_parent_dir(name, match))

    if "sub-dir" in rules:
        transfer.update(series.rule_sub_dir(name, match, rules))

    if "episode-only" in rules:
        guessit.update(series.rule_episode_only(name, guessit))

    if "format-title" in rules:
        transfer.update(series.rule_format_title(
            name, guessit, rules, transfer))

    return transfer, guessit
