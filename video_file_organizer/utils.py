import logging
import guessit
import difflib
import shutil
import os
import shlex

from typing import Union

from video_file_organizer.models import VideoFile, OutputFolder
from video_file_organizer.config import RuleBookFile

logger = logging.getLogger('vfo.utils')


def get_vfile_guessit(vfile: VideoFile):
    """A wrapper for the get_guessit function that uses a VideoFile object

    Args:
        vfile: an instance of VideoFile
    """
    if not isinstance(vfile, VideoFile):
        raise TypeError("vfile needs to be an instance of VideoFile")

    return get_guessit(vfile.name)


def get_guessit(name: str) -> Union[dict, None]:
    """Returns the guessit result for the name of the file passed

    Args:
        name: The filename name
    """
    guessitmatch = dict(guessit.guessit(name))

    if 'title' not in guessitmatch:
        logger.warning(f"Unable to find title for: '{name}'")
        return None

    if 'type' not in guessitmatch:
        logger.warning(f"Unable to find video type for: '{name}'")
        return None

    return guessitmatch


class RuleBookMatcher:
    def __init__(self, rulebookfile):
        if not isinstance(rulebookfile, RuleBookFile):
            raise TypeError(
                "output_folder needs to be an instance of RuleBookFile")

        self.rule_book_file = rulebookfile
        self.configparse = self.rule_book_file.configparse

    def get_vfile_rules(self, vfile: VideoFile):
        if not isinstance(vfile, VideoFile):
            raise TypeError("vfile needs to be an instance of VideoFile")
        if not hasattr(vfile, 'guessit'):
            raise AttributeError("Guessit attribute missing")

        name = vfile.name
        vtype = vfile.guessit['type']
        title = vfile.guessit['title']
        alternative_title = None
        if 'alternative_title' in vfile.guessit:
            alternative_title = vfile.guessit['alternative_title']

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
            title, self.configparse.options('series'),
            n=1, cutoff=DIFF_CUTOFF)

        # Get difflib_match from alternative_title
        if not difflib_match and alternative_title:
            difflib_match = difflib.get_close_matches(
                ' '.join([title, alternative_title]),
                self.configparse.options('series'),
                n=1, cutoff=DIFF_CUTOFF
            )

        # Get the rules from the rule_book with difflib_match
        rules = []
        if difflib_match:
            rules = shlex.split(self.configparse.get(
                'series', difflib_match[0]))

        return rules


class OutputFolderMatcher:
    """Matcher class to scan vfile based on output_folder"""

    def __init__(self, output_folder):
        if not isinstance(output_folder, OutputFolder):
            raise TypeError(
                "output_folder needs to be an instance of OutputFolder")
        self.output_folder = output_folder
        self.entries = self.output_folder.entries

    def get_vfile_match(self, vfile: VideoFile):
        if not isinstance(vfile, VideoFile):
            raise TypeError("vfile needs to be an instance of VideoFile")
        if not hasattr(vfile, 'guessit'):
            raise ValueError("vfile needs to have guessit as an attribute")
        name = vfile.name
        title = vfile.guessit['title']
        return self.get_match(name, title)

    def get_match(self, name: str, title: str) -> Union[dict, None]:
        """Matches the name & title to the output folder specified in __init__

        Args:
            name: The name of the file
            title: The title of the file
        """
        index_match = difflib.get_close_matches(
            title, self.entries.keys(), n=1, cutoff=0.6
        )[0]

        if not index_match:
            logger.warn("Match FAILED: " +
                        f"Unable to find a match for {name}")
            return None

        logger.debug(f"Match successful for {name}")

        return {
            "name": index_match,
            "_entry": self.entries[index_match]['_entry'],
            "sub_entries": self.entries[index_match]['sub_entries']
        }


class Transferer:
    def __init__(self):
        pass

    def __enter__(self):
        self.delete_list = []
        return self

    def __exit__(self, type, value, traceback):
        # Removes duplicates
        self.delete_list = list(set(self.delete_list))

        for source in self.delete_list:
            try:
                os.remove(source)
            except PermissionError:
                # Getting permission error when its a folder
                shutil.rmtree(source)
            logger.info(f"Deleted {os.path.basename(source)}")
        return True

    def transfer_vfile(self, vfile: VideoFile, **kwargs):
        """A wrapper for the transfer function that uses a VideoFile object

        Args:
            vfile: an instance of VideoFile
            **kwargs:
        """
        if not isinstance(vfile, VideoFile):
            raise TypeError("vfile needs to be an instance of VideoFile")
        if not hasattr(vfile, 'transfer'):
            raise ValueError("vfile needs to have transfer as an attribute")
        if 'transfer_to' not in vfile.transfer:
            raise KeyError("transfer_to key missing in transfer attribute")

        if hasattr(vfile, 'root_path'):
            kwargs.update(root_path=getattr(vfile, 'root_path'))

        source = vfile.path
        destination = vfile.transfer['transfer_to']

        self.transfer(source, destination, **kwargs)

    def transfer(self, source: str, destination: str, **kwargs):
        """A function that transfers and deletes a source file to a destination

        Args:
            source: path to source file
            destination: path to destination
            **kwargs:
        """
        self._copy(source, destination, **kwargs)
        self._delete(source, **kwargs)

    def _copy(self, source: str, destination: str, **kwargs):
        """A function that copies a source file to a destination

        Args:
            source: path to source file
            destination: path to destination
            **kwargs:
        """
        logger.info(f"Transfering {os.path.basename(source)} to {destination}")
        shutil.copy(source, destination)

    def _delete(self, source: str, **kwargs):
        """A function that deletes the source file

        Args:
            source: path to source file
            **kwargs:
                delete (bool): Delete the file or not
                root_path (str): Deletes this path instead of source path
        """
        if 'delete' in kwargs.keys() and not kwargs['delete']:
            return

        if 'root_path' in kwargs.keys():
            self.delete_list.append(kwargs['root_path'])
            return

        self.delete_list.append(source)
