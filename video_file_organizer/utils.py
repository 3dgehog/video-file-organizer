import logging
import guessit
import difflib

from video_file_organizer.models import VideoFile

logger = logging.getLogger('app.utils')


def get_vfile_guessit(vfile: VideoFile):
    if not isinstance(vfile, VideoFile):
        raise TypeError("vfile needs to be an instance of VideoFile")

    return get_guessit(vfile.name)


def get_guessit(name: str) -> dict:
    guessitmatch = guessit.guessit(name)

    if 'title' not in guessitmatch:
        logger.warn(f"Unable to find title for: '{name}'")
        return None

    if 'type' not in guessitmatch:
        logger.warn(f"Unable to find video type for: '{name}'")
        return None

    return guessitmatch


class Matcher:
    """Matcher class to scan vfile based on output_folder"""

    def __init__(self, output_folder):
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

    def get_match(self, name: str, title: str) -> dict:
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
