import os
import abc

from typing import Union


class ListOfEntries(metaclass=abc.ABCMeta):
    _entries: list = []

    @property
    def entries(self) -> list:
        if not self._entries:
            self._entries = self._scan_entries()
        return self._entries

    @entries.setter
    def entries(self, entries: list):
        self._entries = entries

    @abc.abstractmethod
    def _scan_entries(self) -> list:
        return []

    def __iter__(self):
        for entry in self.entries:
            yield entry

    def __getitem__(self, key: int):
        if not self.entries:
            self.entries = self._scan_entries()
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

    def list_entries_by_name(self) -> list:
        return [entry.name for entry in self.entries]

    def _map_entry_to_entry_type(
            self, entry: os.DirEntry, video_extensions: list):
        # NOTE: Check if its a Directory
        if entry.is_dir():
            return DirectoryEntry(
                entry.name, entry.path, self.depth + 1, video_extensions)
        else:
            ext = entry.name.rpartition('.')[-1]

            # NOTE: Check if its a Video File
            if ext in video_extensions:
                return VideoFileEntry(
                    entry.name, entry.path, ext, self.depth + 1)
            else:
                return FileEntry(entry.name, entry.path, ext, self.depth + 1)


class InputDirectory(ListOfEntries):
    def __init__(
        self,
        path: str,
        video_extensions: list = [],
        ignore: list = [],
        whitelist: list = []
    ):
        self.path = path
        self.video_extensions = video_extensions
        self.depth = 0
        self.ignore = ignore
        self.whitelist = whitelist

    def _scan_entries(self):
        entries: list = []
        for entry in os.scandir(self.path):

            if entry.name in self.ignore:
                continue
            if self.whitelist:
                if entry.name in self.whitelist:
                    entries.append(self._map_entry_to_entry_type(
                        entry, self.video_extensions))
                continue

            entries.append(self._map_entry_to_entry_type(
                entry, self.video_extensions))
        return entries

    def __repr__(self):
        return f'<{__class__.__name__} {self.path}>'


class OutputDirectories(ListOfEntries):
    def __init__(self, paths: list, video_extensions: list = []):
        self.paths = paths
        self.video_extensions = video_extensions

    def _scan_entries(self):
        entries: list = []
        for path in self.paths:
            for entry in os.scandir(path):
                entries.append(self._map_entry_to_entry_type(
                    entry, self.video_extensions))
        return entries

    def __repr__(self):
        return f'<{__class__.__name__} {self.paths}>'


class DirectoryEntry(ListOfEntries):
    def __init__(
        self,
        name: str,
        path: str,
        depth: int,
        video_extensions: list = []
    ):
        self.name = name
        self.path = path
        self.depth = depth
        self.video_extensions = video_extensions

    def _scan_entries(self):
        entries: list = []
        for entry in os.scandir(self.path):
            entries.append(self._map_entry_to_entry_type(
                entry, self.video_extensions))
        return entries

    def __repr__(self):
        return f'<{__class__.__name__} {self.name}>'


class FileEntry:
    def __init__(self, name: str, path: str, extension: str, depth: int):
        self.name = name
        self.path = path
        self.extension = extension
        self.depth = depth

    def __repr__(self):
        return f'<{__class__.__name__} {self.name}>'


class VideoFileEntry(FileEntry):
    def __init__(self, name: str, path: str, extension: str, depth: int):
        super().__init__(name, path, extension, depth)
        self._metadata: dict = {}
        self.foldermatch: Union[DirectoryEntry, None] = None
        # self.root_path: str = ''
        self.transfer: dict = {}
        self.valid: bool = True
        self.error_msg: str = ''

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, data: dict):
        self._metadata = data

    def __repr__(self):
        return f'<{__class__.__name__} {self.name}>'
