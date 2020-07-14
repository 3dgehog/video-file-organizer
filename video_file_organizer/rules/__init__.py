from video_file_organizer.models import VideoFile

from video_file_organizer.utils import VFileConsumer, Observer


class RuleEntry:
    def __init__(self, name: str, rule_function, when: str):
        self.name = name
        self.rule_function = rule_function
        self.when = when


class RuleCollection(VFileConsumer, Observer):
    def __init__(self):
        self._entries: list = []

    def update(self, *arg, topic: str, **kwargs):
        vfile = kwargs['vfile']

        if topic == 'RuleBookMatcher/after':
            self.before_foldermatch_by_vfile(vfile=vfile)

        if topic == 'OutputFolderMatcher/after':
            self.before_transfer_by_vfile(vfile=vfile)

    def add_handler(self, rule_entry: RuleEntry):
        self._entries.append(rule_entry)

    @VFileConsumer.vfile_consumer('name', 'metadata', 'rules')
    def before_foldermatch_by_vfile(self, vfile: VideoFile, **kwargs) -> dict:
        return self.run_rules('before_foldermatch', **kwargs)

    @VFileConsumer.vfile_consumer(
        'name', 'metadata', 'foldermatch', 'transfer', 'rules')
    def before_transfer_by_vfile(self, vfile: VideoFile, **kwargs) -> dict:
        return self.run_rules('before_transfer', **kwargs)

    def run_rules(self, when: str, **kwargs):
        rules_list: list = []
        for entry in self._entries:
            if entry.when == when:
                rules_list.append(entry)

        for entry in rules_list:
            if entry.name in kwargs['rules']:
                kwargs.update(entry.rule_function(**kwargs))

        return kwargs
