import os
import logging
import abc

from typing import Union, List

logger = logging.getLogger('vfo.mapping')


class EntryList(metaclass=abc.ABCMeta):
    _entries: list = []

    @property
    def entries(self) -> list:
        if not self._entries:
            self._entries = self.scan()
        return self._entries

    @entries.setter
    def entries(self, entries: list):
        self._entries = entries

    @abc.abstractmethod
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
        return [entry.name for entry in self.entries]


class Entry(EntryList):
    def __init__(self, is_parent=True, depth_level=0, **kwargs):

        if 'dir_entry' in kwargs.keys():
            self.by_dir_entry(kwargs['dir_entry'])
        self._dir_entry = kwargs.get('dir_entry') or None

        self.path = kwargs.get('path') or self.path or None
        self.name = kwargs.get('name') or self.name or None
        self.is_dir = kwargs.get('is_dir') or self.is_dir or None
        self.is_file = kwargs.get('is_file') or self.is_file or None

        self.is_parent = is_parent
        self.depth_level = depth_level

        self.file_extension = None
        if self.is_file:
            self.file_extension = self.name.rpartition('.')[-1]

    def by_dir_entry(self, dir_entry: os.DirEntry):
        self.path = dir_entry.path
        self.name = dir_entry.name
        self.is_dir = dir_entry.is_dir()
        self.is_file = dir_entry.is_file()

    def scan(self) -> list:
        """[<Entry>, <Entry>]"""
        data: list = []

        if self.is_file:
            return []

        for entry in os.scandir(self.path):
            data.append(Entry(
                dir_entry=entry,
                depth_level=self.depth_level+1,
                is_parent=False))
        return data

    def __repr__(self) -> str:
        return f"<Entry '{self.name}'>"


class FolderCollection(EntryList):
    def __init__(
        self, path: Union[str, list],
        ignore: list = [],
        whitelist: Union[None, list] = []
    ):

        self.path = path
        # Makes sure path is a list
        if type(path) is str:
            self.path = [self.path]

        self.ignore = ignore
        self.whitelist = whitelist

    def scan(self) -> list:
        """[<Entry>, <Entry>]"""
        data: list = []
        for path in self.path:
            for entry in os.scandir(path):
                if entry.name in self.ignore:
                    continue
                if self.whitelist:
                    if entry.name in self.whitelist:
                        data.append(Entry(dir_entry=entry))
                    continue
                data.append(Entry(dir_entry=entry))
        return data


class VideoCollection(FolderCollection):
    def __init__(
            self,
            path: str,
            ignore: list = [],
            videoextensions: list = [],
            whitelist: Union[None, list] = None
    ):
        if type(path) is not str:
            raise TypeError("Input Folder can only be a single folder")

        super().__init__(path, ignore, whitelist)

        self.videoextensions = videoextensions

        self._vfiles: list = []
        self._scan_vfiles(self.entries)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._purge()

    def _purge(self):
        del_list = [vfile for vfile in self._vfiles if not vfile.valid]
        for vfile in del_list:
            self._vfiles.remove(vfile)
            logger.debug(f"Purged vfile {vfile.name}")

    def _scan_vfiles(self, entries: list) -> list:
        """[<VideoFile>, <Videofile>]"""
        data: List[VideoFile] = []
        for entry in entries:
            if entry.file_extension in self.videoextensions:
                self.add_vfile(
                    entry.name,
                    path=entry.path,
                    root_path=entry.path)
            if entry.is_dir:
                for entry2 in entry:
                    if entry2.file_extension in self.videoextensions:
                        self.add_vfile(
                            entry2.name,
                            path=entry2.path,
                            root_path=entry.path)
        return data

    def add_vfile(self, name: str, **kwargs):
        vfile = VideoFile()
        setattr(vfile, 'name', name)
        if kwargs:
            vfile.update(**kwargs)
        self._vfiles.append(vfile)
        logger.debug(f"Added vfile {name} with kwargs {kwargs}")

    def __iter__(self):
        for vfile in self._vfiles:
            yield vfile


class VideoFile:
    def __init__(self, **kwargs):

        self.name: str = ''
        self.metadata: dict = {}
        self.rules: list = []
        self.foldermatch: Union[Entry, None] = None
        self.path: str = ''
        self.root_path: str = ''
        self.transfer: dict = {}
        self.valid: bool = True
        self.error_msg: str = ''

        if kwargs:
            self.update(**kwargs)

    def update(self, *args, merge: bool = True, **kwargs):
        if args:
            raise ValueError('Update function only takes kwargs')
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise AttributeError(f"Attribute {key} doesn't exist")
            if merge:
                if getattr(self, key) in [list, dict]:
                    orig = getattr(self, key)
                    orig.update(value)
                    value = orig
            setattr(self, key, value)
        logger.debug(f"Updated vfile {self.name} with kwargs {kwargs}")

    @property
    def json(self):
        return {
            'name': self.name,
            'metadata': self.metadata,
            'rules': self.rules,
            'foldermatch': self.foldermatch,
            'path': self.path,
            'root_path': self.root_path,
            'transfer': self.transfer,
            'valid': self.valid,
        }.copy()
