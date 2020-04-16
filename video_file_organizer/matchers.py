import logging
import guessit
import difflib
import shlex

from typing import Union

from video_file_organizer.models import VideoFile, FolderCollection
from video_file_organizer.config import RuleBookFile

logger = logging.getLogger('vfo.matachers')


class MetadataMatcher:
    def __call__(self, vfile: VideoFile):
        return self.match_vfile(vfile)

    def match_vfile(self, vfile: VideoFile):
        """A wrapper for the get_guessit function that uses a VideoFile object
        """
        return self.get_guessit(vfile.name)

    def get_guessit(self, name: str) -> Union[dict, None]:
        """Returns the guessit result for the name of the file passed

        Args:
            name: The filename name
        """
        results = dict(guessit.guessit(name))

        if 'title' not in results:
            logger.warning(f"Unable to find title for: '{name}'")
            return None

        if 'type' not in results:
            logger.warning(f"Unable to find video type for: '{name}'")
            return None

        return results


class RuleBookMatcher:
    def __init__(self, rulebookfile):

        if not isinstance(rulebookfile, RuleBookFile):
            raise TypeError(
                "output_folder needs to be an instance of RuleBookFile")

        self.rulebook = rulebookfile

    def __call__(self, vfile: VideoFile):
        return self.match_vfile(vfile)

    def match_vfile(self, vfile: VideoFile):
        if not hasattr(vfile, 'metadata'):
            raise AttributeError("Metadata attribute missing")

        name = vfile.name
        vtype = vfile.metadata['type']
        title = vfile.metadata['title']
        alternative_title = None
        if 'alternative_title' in vfile.metadata:
            alternative_title = vfile.metadata['alternative_title']

        return self.get_rules(name, vtype, title, alternative_title)

    def get_rules(
            self, name: str, vtype: str, title: str,
            alternative_title: str = None) -> list:
        VALID_TYPES = {"episode": self._get_series_rules}

        rules = []
        for key, func in VALID_TYPES.items():
            if vtype == key:
                rules = func(name, title, alternative_title)

        if len(rules) == 0:
            logger.warn(f"Unable to find the rules for: {name}")
            return None

        return rules

    def _get_series_rules(
            self, name, title=None, alternative_title=None) -> list:
        """Uses the title from the fse to try to match to its rules type from the
        rule_book.ini"""
        if title is None:
            return []

        # Get difflib_match from title
        DIFF_CUTOFF = 0.7
        difflib_match = difflib.get_close_matches(
            title, self.rulebook.list_of_series(),
            n=1, cutoff=DIFF_CUTOFF)

        # Get difflib_match from alternative_title
        if not difflib_match and alternative_title:
            difflib_match = difflib.get_close_matches(
                ' '.join([title, alternative_title]),
                self.rulebook.list_of_series(),
                n=1, cutoff=DIFF_CUTOFF
            )

        # Get the rules from the rule_book with difflib_match
        rules = []
        if difflib_match:
            rules = shlex.split(
                self.rulebook.get_series_rule(difflib_match[0]))

        return rules


class OutputFolderMatcher:
    """Matcher class to scan vfile based on output_folder"""

    def __init__(self, output_folder):

        if not isinstance(output_folder, FolderCollection):
            raise TypeError(
                "output_folder needs to be an instance of OutputFolder")
        self.output_folder = output_folder
        self.entries = self.output_folder.entries

    def __call__(self, vfile: VideoFile):
        return self.match_vfile(vfile)

    def match_vfile(self, vfile: VideoFile):
        if not hasattr(vfile, 'metadata'):
            raise ValueError("vfile needs to have metadata as an attribute")
        name = vfile.name
        title = vfile.metadata['title']
        return self.get_match(name, title)

    def get_match(self, name: str, title: str) -> Union[dict, None]:
        """Matches the name & title to the output folder specified in __init__

        Args:
            name: The name of the file
            title: The title of the file
        """
        index_match = difflib.get_close_matches(
            title, self.output_folder.list_entry_names(), n=1, cutoff=0.6
        )[0]

        if not index_match:
            logger.warn("Match FAILED: " +
                        f"Unable to find a match for {name}")
            return None

        logger.debug(f"Match successful for {name}")

        return self.output_folder[index_match]
