import os
import logging

from typing import Union, List

logger = logging.getLogger('vfo.models')


class BaseFolder:
    _entries: list = []

    @property
    def entries(self) -> list:
        if not self._entries:
            self._entries = self.scan()
        return self._entries

    @entries.setter
    def entries(self, entries: list):
        self._entries = entries

    def scan(self) -> list:
        return []

    def __iter__(self):
        for entry in self.entries:
            yield entry

    def __getitem__(self, key: int):
        if not self.entries:
            self.entries = self.scan()
        return self.entries[key]

    def __delitem__(self, key: Union[int, str]):
        pass

    def __setitem__(self, key: Union[int, str]):
        pass

    def __len__(self) -> int:
        return len(self.entries)

    def get_entry_by_name(self, name: str):
        for entry in self.entries:
            if entry.name == name:
                return entry
        raise KeyError(f"Couldn't find an entry with the name '{name}'")

    def list_entry_names(self) -> list:
        data: list = []
        for entry in self.entries:
            data.append(entry.name)
        return data


class FolderEntry(BaseFolder):
    def __init__(self, dir_entry: os.DirEntry):

        self._dir_entry = dir_entry

        self.path = self._dir_entry.path
        self.name = self._dir_entry.name
        self.is_dir = self._dir_entry.is_dir
        self.is_file = self._dir_entry.is_file
        self._entries: list = []

    def scan(self) -> list:
        """[<FolderEntry>, <FolderEntry>]"""
        data: list = []
        for entry in os.scandir(self.path):
            data.append(FolderEntry(entry))
        return data

    def __repr__(self) -> str:
        return f"<FolderEntry '{self.name}'>"


class FolderCollection(BaseFolder):
    def __init__(self, path: Union[str, list], ignore: list = []):

        self.path = path
        # Makes sure path is a list
        if type(path) is str:
            self.path = [self.path]

        self.ignore = ignore
        self._entries = self.scan()

    def scan(self) -> list:
        """[<FolderEntry>, <FolderEntry>]"""
        data: list = []
        for path in self.path:
            for entry in os.scandir(path):
                if entry.name in self.ignore:
                    continue
                data.append(FolderEntry(entry))
        return data


class VideoCollection(FolderCollection):
    def __init__(
            self,
            path: str,
            ignore: list = [],
            videoextensions: list = []
    ):
        if type(path) is not str:
            raise TypeError("Input Folder can only be a single folder")

        super().__init__(path, ignore)

        self.videoextensions = videoextensions

        self._vfiles: list = []
        self._scan_vfiles(self.entries)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._purge()

    def _purge(self):
        del_list: list = []
        for vfile in self._vfiles:
            if not vfile.valid:
                del_list.append(vfile)
        for vfile in del_list:
            self._vfiles.remove(vfile)
            logger.debug(f"Purged vfile {vfile.name}")

    def _scan_vfiles(self, entries: list) -> list:
        """[<VideoFile>, <Videofile>]"""
        data: List[VideoFile] = []
        for entry in entries:
            if entry.name.rpartition('.')[-1] in self.videoextensions:
                self.add_vfile(
                    entry.name,
                    path=entry.path,
                    root_path=entry.path)
            if entry.is_dir():
                for entry2 in entry:
                    if entry2.name.rpartition('.')[-1] in self.videoextensions:
                        self.add_vfile(
                            entry2.name,
                            path=entry2.path,
                            root_path=entry.path)
        return data

    def add_vfile(self, name: str, **kwargs):
        vfile = VideoFile()
        setattr(vfile, 'name', name)
        if kwargs:
            vfile.edit(**kwargs)
        self._vfiles.append(vfile)
        logger.debug(f"Added vfile {name} with kwargs {kwargs}")

    def get_vfile(self, name: str):
        for vfile in self._vfiles:
            if vfile.name == name:
                return vfile
        raise ValueError("This video file doesn't exists in list")

    def __iter__(self):
        for vfile in self._vfiles:
            yield vfile


class VideoFile:
    def __init__(self, **kwargs):
        self.name: str = ''
        self.metadata: dict = {}
        self.rules: list = []
        self.foldermatch: Union[FolderEntry, None] = None
        self.path: str = ''
        self.root_path: str = ''
        self.transfer: dict = {}
        self.valid = True

        if kwargs:
            self.edit(**kwargs)

    def edit(self, *args, merge: bool = True, **kwargs):
        if args:
            raise ValueError('edit function only takes kwargs')
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise AttributeError(f"Attribute {key} is not valid")
            if merge:
                if getattr(self, key) in [list, dict]:
                    orig = getattr(self, key)
                    orig.update(value)
                    value = orig
            setattr(self, key, value)
        logger.debug(f"Edited vfile {self.name} with kwargs {kwargs}")

    def get_attr(self, *args) -> dict:
        data: dict = {}
        for arg in args:
            if not hasattr(self, arg):
                raise AttributeError(f"Attribute {arg} is not valid")
            data.update({arg: getattr(self, arg)})
        return data
