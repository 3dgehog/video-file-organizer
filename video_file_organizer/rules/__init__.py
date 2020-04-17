from video_file_organizer.models import VideoFile

from video_file_organizer.rules import series
from video_file_organizer.utils import vfile_options


class RuleEntry:
    def __init__(self, name: str, rule_function, when: str):
        self.name = name
        self.rule_function = rule_function
        self.when = when


class RuleCollection:
    def __init__(self):
        self._entries: list = []
        self.add_series_rules()

    def add_handler(self, rule_entry: RuleEntry):
        self._entries.append(rule_entry)

    def add_series_rules(self):
        self.add_handler(
            RuleEntry('season', series.rule_season, 'before_transfer'))
        self.add_handler(
            RuleEntry('parent-dir', series.rule_parent_dir, 'before_transfer'))
        self.add_handler(
            RuleEntry('sub-dir', series.rule_sub_dir, 'before_transfer'))
        self.add_handler(
            RuleEntry(
                'episode-only',
                series.rule_episode_only,
                'before_transfer')
        )
        self.add_handler(
            RuleEntry(
                'format-title',
                series.rule_format_title,
                'before_transfer')
        )
        self.add_handler(
            RuleEntry(
                'alt-title',
                series.rule_alt_title,
                'before_foldermatch')
        )

    @vfile_options('name', 'metadata')
    def before_foldermatch(self, vfile: VideoFile, **kwargs) -> dict:
        rules_list: list = []
        for entry in self._entries:
            if entry.when == 'before_foldermatch':
                rules_list.append(entry)

        for entry in rules_list:
            if entry.name in vfile.rules:
                kwargs.update(entry.rule_function(**kwargs))

        return kwargs

    @vfile_options('name', 'metadata', 'foldermatch', 'rules', 'transfer')
    def before_transfer(self, vfile: VideoFile, **kwargs) -> dict:
        rules_list: list = []
        for entry in self._entries:
            if entry.when == 'before_transfer':
                rules_list.append(entry)

        for entry in rules_list:
            if entry.name in vfile.rules:
                kwargs.update(entry.rule_function(**kwargs))

        return kwargs
