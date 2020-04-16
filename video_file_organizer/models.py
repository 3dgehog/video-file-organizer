import os
import posix
from typing import Union, Dict
import logging

logger = logging.getLogger('vfo.models')


class FolderBase:
    def __iter__(self):
        for entry in self.entries:
            yield entry

    def __getitem__(self, key):
        if not self.entries:
            print('scanning folder')
            self.entries = self.scan()

        if type(key) is str:
            for entry in self.entries:
                if entry.name == key:
                    return entry
            raise KeyError(key)

        return self.entries[key]

    def __delitem__(self, key):
        pass

    def __setitem__(self, key):
        pass

    def __len__(self):
        return len(self.entries)

    def list_entry_names(self):
        data: list = []
        for entry in self.entries:
            data.append(entry.name)
        return data


class FolderCollection(FolderBase):
    def __init__(self, path: Union[str, list], ignore: list = []):

        self.path = path
        # Makes sure path is a list
        if type(path) is str:
            self.path = [self.path]

        self.ignore = ignore
        self.entries = self.scan(self.path)

    def scan(self, paths: list):
        """Returns
        [<FolderEntry>, <FolderEntry>]
        """
        data: list = []
        for path in paths:
            for entry in os.scandir(path):
                if entry.name in self.ignore:
                    continue
                data.append(FolderEntry(entry))
        return data


class FolderEntry(FolderBase):
    def __init__(self, dir_entry: posix.DirEntry):

        self._dir_entry = dir_entry

        self.path = self._dir_entry.path
        self.name = self._dir_entry.name
        self.is_dir = self._dir_entry.is_dir
        self.is_file = self._dir_entry.is_file
        self._entries = None

    @property
    def entries(self):
        if not self._entries:
            self._entries = self.scan()
        return self._entries

    @entries.setter
    def entries(self, entries):
        self._entries = entries

    def scan(self):
        """Returns
        [<FolderEntry>, <FolderEntry>]
        """
        data: list = []
        for entry in os.scandir(self.path):
            data.append(FolderEntry(entry))
        return data

    def __repr__(self):
        return f"<FolderEntry '{self.name}'>"


class InputFolder(FolderCollection):
    def __init__(
            self, path: str, ignore: list = [],
            videoextensions: list = []) -> None:

        if type(path) is not str:
            raise TypeError("Input Folder can only be a single folder")
        super().__init__(path, ignore)

        self.videoextensions = videoextensions

        self._vfiles: Dict[str, Union[VideoFile, None]] = {}
        self._scan_vfiles(self.entries)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._purge()

    def _purge(self):
        """Removes all dictionary entries from self._vfile where the
        Videofile is missing"""
        del_list = [x for x in self._vfiles.items(
        ) if not isinstance(x[1], VideoFile)]
        for name in del_list:
            self._vfiles.pop(name, None)
            logger.debug(f"Purged vfile {name}")

    def _scan_vfiles(self, entries: list):
        """
        Returns a dict with this format
        {
            "name": <VideoFile>
        }
        """
        data: dict = {}
        for entry in entries:
            if entry.name.rpartition('.')[-1] in self.videoextensions:
                self.add_vfile(entry.name, path=entry.path)
            if entry.is_dir():
                for entry2 in entry:
                    if entry2.name.rpartition('.')[-1] in self.videoextensions:
                        self.add_vfile(
                            entry2.name,
                            path=entry2.path,
                            root_path=entry.path)
        return data

    def add_vfile(self, name, **kwargs):
        if name in self._vfiles.keys():
            raise ValueError("This video file already exists in list")
        vfile = VideoFile()
        setattr(vfile, 'name', name)
        for key, value in kwargs.items():
            setattr(vfile, key, value)
        self._vfiles[name] = vfile
        logger.debug(f"Added vfile {name} with kwargs {kwargs}")

    def get_vfile(self, name):
        if name not in self._vfiles.keys():
            raise ValueError("This video file doesn't exists in list")
        return self._vfiles[name]

    def remove_vfile(self, name: str):
        if name not in self._vfiles.keys():
            raise ValueError("This video file doesn't exist in list")
        self._vfiles[name] = None
        logger.debug(f"Removed vfile {name} ")

    def iter_vfiles(self):
        for name, vfile in self._vfiles.items():
            yield name, vfile


class VideoFile:
    def __init__(self):
        self.name: str = ''
        self.metadata: dict = {}
        self.rules: list = []
        self.foldermatch: Union[FolderEntry, None] = None
        self.path: str = ''
        self.transfer: dict = {}

    def edit(self, merge: bool = True, **kwargs):
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise AttributeError("Attribute {name} is not valid")
            if merge:
                if getattr(self, key) in [list, dict]:
                    orig = getattr(self, key)
                    orig.update(value)
                    value = orig
        setattr(self, key, value)
        logger.debug(f"Edited vfile {self.name} with kwargs {kwargs}")
