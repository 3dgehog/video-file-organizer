from video_file_organizer.models import VideoFile

from video_file_organizer.utils import VFileAddons, Observer


class RuleEntry:
    def __init__(self, name: str, rule_function, topic: str):
        self.name = name
        self.rule_function = rule_function
        self.topic = topic


class RuleRegistry(Observer):
    _entries: list = []

    def update(self, *arg, topic: str, **kwargs):
        if 'RuleRegistry' not in topic:
            self.run_rules(topic=topic, **kwargs)

    @classmethod
    def add_rule(cls, name, function, topic):
        cls._entries.append(
            RuleEntry(
                name=name,
                rule_function=function,
                topic=topic
            )
        )

    @VFileAddons.vfile_consumer
    def run_rules(self, vfile: VideoFile, topic: str, **kwargs):
        rules_list: list = []
        for entry in self._entries:
            if entry.topic == topic:
                rules_list.append(entry)

        for entry in rules_list:
            if entry.name in kwargs['rules']:
                kwargs.update(entry.rule_function(**kwargs))

        return kwargs
