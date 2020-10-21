import logging
import guessit
import difflib

from video_file_organizer.mapping import FolderCollection
from video_file_organizer.config import RuleBook
from video_file_organizer.utils import error_msg

logger = logging.getLogger('vfo.matachers')


class MetadataMatcher:
    def __init__(self):
        pass

    def __call__(self, **kwargs) -> dict:
        return self.get_guessit(**kwargs)

    def get_guessit(self, name: str, **kwargs) -> dict:

        results = dict(guessit.guessit(name))

        if 'title' not in results:
            return error_msg(f"Unable to find title for: '{name}'")

        if 'type' not in results:
            return error_msg(f"Unable to find video type for: '{name}'")

        return {'metadata': results}


class RuleBookMatcher:
    def __init__(self, rulebookfile: RuleBook):
        self.rulebook = rulebookfile

    def __call__(self, **kwargs) -> dict:
        return self.get_rules(**kwargs)

    def get_rules(
            self, name: str, metadata: dict, **kwargs) -> dict:

        VALID_TYPES = {"episode": self._get_series_rules}

        rules = []
        for key, func in VALID_TYPES.items():
            if metadata.get('type') == key:
                rules = func(
                    name,
                    metadata.get('title'),
                    metadata.get('alternative_title')
                )

        if len(rules) == 0:
            return error_msg(f"Unable to find the rules for: {name}")

        return {'rules': rules}

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


class OutputFolderMatcher:
    def __init__(self, output_folder: FolderCollection):
        self.output_folder = output_folder

    def __call__(self, **kwargs) -> dict:
        return self.get_match(**kwargs)

    def get_match(
            self, name: str, metadata: dict, **kwargs) -> dict:
        index_match = difflib.get_close_matches(
            metadata['title'],
            self.output_folder.list_entry_names(),
            n=1, cutoff=0.6
        )

        if not index_match:
            return error_msg(f"Unable to find a match for {name}")

        logger.debug(f"Match successful for {name}")

        return {
            'foldermatch': self.output_folder.get_entry_by_name(
                str(index_match[0])
            )
        }
