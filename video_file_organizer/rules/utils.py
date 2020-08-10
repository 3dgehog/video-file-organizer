from video_file_organizer.models import VideoFile

from video_file_organizer.utils import VFileAddons, Observer


class RuleEntry:
    def __init__(self, name: str, rule_function, topic: str, order: int):
        self.name = name
        self.rule_function = rule_function
        self.topic = topic
        self.order = order


class RuleRegistry(Observer):
    _entries: list = []

    def update(self, *arg, topic: str, **kwargs):
        if 'RuleRegistry' not in topic:
            self.run_rules(topic=topic, **kwargs)

    @classmethod
    def add_rule(cls, name, function, topic, order=10):
        new_entry = RuleEntry(
            name=name,
            rule_function=function,
            topic=topic,
            order=order
        )

        for entry in cls._entries:
            if entry.order > order:
                cls._entries.insert(
                    cls._entries.index(entry)-1,
                    new_entry
                )
                return

        cls._entries.append(
            RuleEntry(
                name=name,
                rule_function=function,
                topic=topic,
                order=order
            )
        )

    @VFileAddons.vfile_consumer
    def run_rules(self, vfile: VideoFile, topic: str, **kwargs):
        rules_list: list = []
        for entry in self._entries:
            if entry.topic == topic:
                rules_list.append(entry)

        if len(rules_list) == 0:
            return True

        for entry in rules_list:
            if entry.name in kwargs['rules']:
                kwargs.update(entry.rule_function(**kwargs))

        return kwargs
