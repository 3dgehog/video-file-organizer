import logging
import guessit
import difflib
from typing import Union

from video_file_organizer.models import VideoFile
logger = logging.getLogger('app.utils')


def scan_vfile(
        name: Union[str, None] = None,
        vfile: Union[VideoFile, None] = None) -> dict:

    if vfile:
        if not isinstance(vfile, VideoFile):
            raise TypeError("vfile needs to be an instance of VideoFile")
        name = vfile.name

    if name is None:
        logging.warn("name or vfile has to passed for this function to work")
        return None

    guessitmatch = guessit.guessit(name)

    if 'title' not in guessitmatch:
        logger.log(11, "NO TITLE MATCH: ",
                   f"Unable to find title for: '{name}'")
        return None

    if 'type' not in guessitmatch:
        logger.log(11, "NO TYPE MATCH: ",
                   f"Unable to find type of video for: '{name}'")
        return None

    return guessitmatch


class Matcher:
    """Matcher class to scan vfile based on output_folder"""

    def __init__(self, output_folder):
        self.output_folder = output_folder

        self.entries = self.output_folder.entries

    def scan_vfile(
            self,
            name: Union[str, None] = None,
            title: Union[str, None] = None,
            vfile: Union[VideoFile, None] = None
    ):

        if vfile:
            if not isinstance(vfile, VideoFile):
                raise TypeError("vfile needs to be an instance of VideoFile")
            name = vfile.name
            title = vfile.guessit['title']

        if title is None or name is None:
            return None

        index_match = difflib.get_close_matches(
            title, self.entries.keys(), n=1, cutoff=0.6
        )[0]

        if not index_match:
            logger.log(11, "FAILED MATCH: " +
                       f"Unable to find a match: {name}")
            return None

        logger.debug(f"Match successful for {name}")

        return {
            "name": index_match,
            "_entry": self.entries[index_match]['_entry']
        }
