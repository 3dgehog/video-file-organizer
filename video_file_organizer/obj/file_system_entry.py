import os
import logging

logger = logging.getLogger('app.fse')


class FileSystemEntry:
    """
    The Object that takes care of the File System Entry in the Input Folder
    - path_to_fse: abspath path to fse
    """

    def __init__(self, input_dir, item: str) -> None:
        self.input_dir = input_dir
        self.name = item

        self.abspath = os.path.join(self.input_dir, item)
        self.isdir = os.path.isdir(self.abspath)

        self.valid = True

        self.vfile = VideoFile()
        self.vfile.filename = None
        self.vfile.abspath = None

        self.title = None
        self.type = None
        self.details = None

        # For matcher
        self.matched_dir_path = None
        self.matched_dir_name = None
        self.matched_dir_entry = None
        # For transferer
        self.transfer_to = None


class VideoFile:
    def __init__(self):
        self.filename = None
        self.abspath = None
