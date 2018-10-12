import os
from typing import Union, List


class DirIndex:
    def __init__(self, path: Union[str, List[str]], subdirs=False) -> None:
        self.path = path

        self.dict: dict = {}
        self.entries: list = []
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
            dir_entry = DirEntry(os.path.join(entry, folder))
            self.dict[folder] = dir_entry
            self.entries.append(dir_entry)


class DirEntry:
    def __init__(self, path: str) -> None:
        self.path = path
        self.name = os.path.basename(path)
        self.subdirs: list = []
        self._get_subdirs()

    def _get_subdirs(self):
        for subfolder in os.listdir(self.path):
            self.subdirs.append(subfolder)
