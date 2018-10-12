import guessit
import os
import logging
from typing import Union


class FileSystemEntry:
    """
    The Object that takes care of the File System Entry in the Input Folder
    - path_to_fse: abspath path to fse
    """

    def __init__(self, app, item: str) -> None:
        self.app = app
        self.config = app.config
        self.name = item

        self.abspath = os.path.join(app.config.input_dir, item)
        self.isdir = os.path.isdir(self.abspath)

        self.valid = True

        self.vfile = VideoFile()
        self.vfile.filename = None
        self.vfile.abspath = None
        self._scan_fse_files()

        self.title = None
        self.type = None
        self.details = None
        self._scan_fse_details()

        self.rules = self._get_fse_rules()

        self.matched_dir_path = None
        self.matched_dir_name = None
        self.matched_dir_entry = None

    def _scan_fse_files(self):
        """Scans FSE and validates it. If its a valid object, self.valid will
        be set to true"""
        if self.isdir:
            for item in os.listdir(self.abspath):
                # if secondary directory, ignore
                if os.path.isdir(os.path.join(self.abspath, item)):
                    continue

                # if file has file extension
                if self.config.re_file_ext_pattern.match(item):
                    # if file was already valid, break and set to not valid
                    # reason: does not support multiple files right now!!
                    if self.vfile.filename:
                        self.valid = False
                        break
                    self.vfile.filename = item
                    self.vfile.abspath = os.path.join(self.abspath, item)

        else:
            # check if the file found has a valid file extension
            if self.config.re_file_ext_pattern.match(self.name):
                self.vfile.filename = self.name
                self.vfile.abspath = self.abspath

    def _scan_fse_details(self):
        """Scans the FSE filename and foldername to guess all the details
        about it. """
        guessitmatch = guessit.guessit(self.vfile.filename)

        if self.isdir:
            # Guess the dir name
            guessitmatch_foldername = guessit.guessit(self.name)
            # keep the better guess from the filename or the foldername
            if len(guessitmatch_foldername) > len(guessitmatch):
                guessitmatch = guessitmatch_foldername
                logging.debug(
                    "used foldername instead of filename for guessit match.")
        self.details = guessitmatch

        # Try to set the title from the guessitmatch
        try:
            self.title = guessitmatch['title']
            self.type = guessitmatch['type']
        except KeyError:
            logging.warning(
                "error trying to find title or type for '{}'".format(
                    self.vfile.filename))
            logging.debug(
                "error guessit match dict '{}'".format(self.details))
            self.valid = False

    def _get_fse_rules(self) -> Union[dict, None]:
        rules = None
        if self.type == "episode":
            rules = self.app.rule_book.get_series_rules_by_title(self.title)

        if rules is None:
            self.valid = False

        return rules


class VideoFile:
    def __init__(self):
        self.filename = None
        self.abspath = None
