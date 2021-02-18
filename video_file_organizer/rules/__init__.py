import logging

from video_file_organizer.entries import VideoFileEntry
from video_file_organizer.utils import Observer, Observee

from video_file_organizer.rules import series

logger = logging.getLogger('vfo.rules')


class RuleEntry:
    def __init__(self, name: str, rule_function, topic: str, order: int):
        self.name = name
        self.rule_function = rule_function
        self.topic = topic
        self.order = order

    def __repr__(self):
        return f"<RuleEntry {self.name} {self.topic} {self.order}"


class RuleRegistry(Observer, Observee):
    def __init__(self):
        super().__init__()

        self._entries: list = []

        self.add_rule(
            'season',
            series.rule_season,
            'OutputFolderMatcher/after',
            10
        )
        self.add_rule(
            'parent-dir',
            series.rule_parent_dir,
            'OutputFolderMatcher/after',
            10
        )
        self.add_rule(
            'sub-dir',
            series.rule_sub_dir,
            'OutputFolderMatcher/after',
            10
        )
        self.add_rule(
            'episode-only',
            series.rule_episode_only,
            'OutputFolderMatcher/after',
            20
        )
        self.add_rule(
            'format-title',
            series.rule_format_title,
            'OutputFolderMatcher/after',
            20
        )
        self.add_rule(
            'alt-title',
            series.rule_alt_title,
            'RuleBookMatcher/after',
            20
        )

        logger.debug(f"List of all added rules: {self._entries}")

    def update(self, *arg, topic: str, **kwargs):
        rules_list = [x for x in self._entries if x.topic == topic]
        if len(rules_list) < 1:
            return
        self._run_rules(topic=topic, rules_list=rules_list, **kwargs)

    def add_rule(self, name, function, topic, order=10):
        new_entry = RuleEntry(name=name, rule_function=function,
                              topic=topic, order=order)

        for entry in self._entries:
            if entry.order > order:
                self._entries.insert(
                    self._entries.index(entry)-1,
                    new_entry
                )
                return

        self._entries.append(new_entry)

    def _run_rules(self, vfile: VideoFileEntry, topic: str, rules_list: list,
                   **kwargs):
        for entry in rules_list:
            if entry.name in vfile.rules:
                if not vfile.valid:
                    return

                with self:
                    self.notify_observers(
                        topic=f'Rule/{entry.name}/before',
                        vfile=vfile)

                    logger.debug(
                        f"RULE '{entry.name}' applying to {vfile.name}")

                    entry.rule_function(vfile=vfile)

                    if not vfile.valid:
                        return

                    logger.debug(f"RULE '{entry.name}' OK for {vfile.name}")

                    self.notify_observers(
                        topic=f'Rule/{entry.name}/after',
                        vfile=vfile)
