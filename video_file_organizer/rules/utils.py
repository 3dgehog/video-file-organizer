from video_file_organizer.entries import VideoFileEntry

from video_file_organizer.utils import Observer, Observee


class RuleEntry:
    def __init__(self, name: str, rule_function, topic: str, order: int):
        self.name = name
        self.rule_function = rule_function
        self.topic = topic
        self.order = order


class RuleRegistry(Observer, Observee):
    _entries: list = []

    def update(self, *arg, topic: str, **kwargs):
        rules_list = [x for x in self._entries if x.topic == topic]
        if len(rules_list) < 1:
            return
        self._run_rules(topic=topic, rules_list=rules_list, **kwargs)

    @classmethod
    def add_rule(cls, name, function, topic, order=10):
        new_entry = RuleEntry(name=name, rule_function=function,
                              topic=topic, order=order)

        for entry in cls._entries:
            if entry.order > order:
                cls._entries.insert(
                    cls._entries.index(entry)-1,
                    new_entry
                )
                return

        cls._entries.append(new_entry)

    def _run_rules(self, vfile: VideoFileEntry, topic: str, rules_list: list,
                   **kwargs):
        for entry in rules_list:
            if entry.name in vfile.rules:

                self.notify_observers(
                    topic=f'Rule/{entry.name}/before',
                    vfile=vfile)

                entry.rule_function(vfile=vfile)

                self.notify_observers(
                    topic=f'Rule/{entry.name}/after',
                    vfile=vfile)

                if not vfile.valid:
                    return
