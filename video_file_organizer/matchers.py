import logging
import guessit
import difflib

from video_file_organizer.entries import OutputDirectories
from video_file_organizer.config import RuleBook
from video_file_organizer.entries import VideoFileEntry
from video_file_organizer.utils import VideoFileOperation

logger = logging.getLogger('vfo.matachers')


class GuessItMatcher(VideoFileOperation):
    def __init__(self):
        pass

    def __call__(self, vfile: VideoFileEntry):

        results = dict(guessit.guessit(vfile.name))

        if 'title' not in results:
            vfile.error(f"Unable to find title for: '{vfile.name}'")
            return

        if 'type' not in results:
            vfile.error(f"Unable to find video type for: '{vfile.name}'")
            return

        vfile.update(metadata=results)


class RuleBookMatcher(VideoFileOperation):
    def __init__(self, rulebookfile: RuleBook):
        self.rulebook = rulebookfile

    def __call__(self, vfile: VideoFileEntry):
        VALID_TYPES = {"episode": self._get_series_rules}

        rules = []
        for key, func in VALID_TYPES.items():
            if vfile.metadata.get('type') == key:
                rules = func(
                    vfile.name,
                    vfile.metadata.get('title'),
                    vfile.metadata.get('alternative_title')
                )

        if len(rules) == 0:
            vfile.error(f"Unable to find the rules for: {vfile.name}")
            return

        vfile.update(rules=rules)

    def _get_series_rules(self, name, title=None,
                          alternative_title=None) -> list:

        if title is None:
            return []

        # Get difflib_match from title
        DIFF_CUTOFF = 0.7
        difflib_match = difflib.get_close_matches(
            title, self.rulebook.list_of_series_name,
            n=1, cutoff=DIFF_CUTOFF)

        # Get difflib_match from alternative_title
        if not difflib_match and alternative_title:
            difflib_match = difflib.get_close_matches(
                ' '.join([title, alternative_title]),
                self.rulebook.list_of_series_name,
                n=1, cutoff=DIFF_CUTOFF
            )

        # Get the rules from the rule_book with difflib_match
        rules: list = []
        if difflib_match:
            rules = self.rulebook.get_series_rule_by_name(
                str(difflib_match[0])
            )

        return rules


class OutputFolderMatcher(VideoFileOperation):
    def __init__(self, output_folder: OutputDirectories):
        self.output_folder = output_folder

    def __call__(self, vfile: VideoFileEntry):
        index_match = difflib.get_close_matches(
            vfile.metadata['title'],
            self.output_folder.list_entries_by_name(),
            n=1, cutoff=0.6
        )

        if not index_match:
            vfile.error(f"Unable to find a match for {vfile.name}")
            return

        logger.debug(f"Match successful for {vfile.name}")

        vfile.update(
            foldermatch=self.output_folder.get_entry_by_name(
                str(index_match[0])
            )
        )
