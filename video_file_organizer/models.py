import os
from typing import Union, List


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


class DirIndex:
    def __init__(self, path: Union[str, List[str]], subdirs=False) -> None:
        self.path = path

        self.dict = {}
        self.entries = []
        self._get_dict_and_entries()
        self.keys = self.dict.keys()

    def _get_dict_and_entries(self):
        """A dict with {"folder_name": DirEntry}"""
        if type(self.path) is not list:
            self._index_single_dir()
        else:
            for entry in self.path:
                self._index_single_dir(entry)

    def _index_single_dir(self, entry=None):
        """appends all entries to self.index"""
        if not entry:
            entry = self.path

        # List through entire folder
        for folder in os.listdir(entry):
            if folder in self.dict.keys():
                raise KeyError("Duplicate folder '{}'".format(folder))
            if os.path.isfile(os.path.join(entry, folder)):
                continue
            dir_entry = DirEntry(os.path.join(entry, folder))
            self.dict[folder] = dir_entry
            self.entries.append(dir_entry)


class DirEntry:
    def __init__(self, path: str) -> None:
        self.path = path
        self.name = os.path.basename(path)
        self.subdirs = []
        self._get_subdirs()

    def _get_subdirs(self):
        for subfolder in os.listdir(self.path):
            self.subdirs.append(subfolder)
