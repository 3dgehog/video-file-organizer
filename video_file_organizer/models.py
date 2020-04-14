import os
from typing import Union, Dict
import logging

logger = logging.getLogger('vfo.models')


class Folder:
    """A representation of a generic folder"""

    def __init__(self, path: Union[str, list], ignore=[]):
        self.path = path
        # Makes sure path is a list
        if type(path) is str:
            self.path = [self.path]

        self.ignore = ignore
        self.entries = self.scan(self.path)

    def scan(self, paths: list) -> dict:
        """
        Returns a dict with this format
        {
            "<name>": {
                "_entry": <DirEntry>
                "sub_entries": {
                    "<name>": {
                        "_entry" : <DirEntry>
                    }
                }
            }
        }
        """
        data = {}
        for path in paths:
            for entry in os.scandir(path):
                if entry.name in self.ignore:
                    continue
                sub_entries = {}
                if entry.is_dir():
                    for sub_entry in os.scandir(entry.path):
                        sub_entries[sub_entry.name] = {'_entry': sub_entry}
                data[entry.name] = {
                    '_entry': entry, 'sub_entries': sub_entries
                }
        return data

        def iterate_entries(self):
            for name, data in self.entries.items():
                yield name, data


class OutputFolder(Folder):
    def __init__(self, path: Union[str, list], ignore=[]):
        super().__init__(path, ignore)


class InputFolder(Folder):
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
        return True

    def _purge(self):
        """Removes all dictionary entries from self._vfile where the
        Videofile is missing"""
        del_list = [x for x in self._vfiles.items(
        ) if not isinstance(x[1], VideoFile)]
        for name in del_list:
            self._vfiles.pop(name, None)
            logger.debug(f"Purged vfile {name}")

    def _scan_vfiles(self, entries: dict):
        """
        Returns a dict with this format
        {
            "name": <VideoFile>
        }
        """
        data: dict = {}
        for fname, fdata in entries.items():
            if fname.rpartition('.')[-1] in self.videoextensions:
                self.add_vfile(fname, path=fdata['_entry'].path)
            if fdata['_entry'].is_dir():
                for sub_fname, sub_fdata in fdata['sub_entries'].items():
                    if sub_fname.rpartition('.')[-1] in self.videoextensions:
                        self.add_vfile(
                            sub_fname,
                            path=sub_fdata['_entry'].path,
                            root_path=fdata['_entry'].path)
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

    def edit_vfile(self, name: str, merge: bool = True, **kwargs):
        if name not in self._vfiles.keys():
            raise ValueError("This video file doesn't exist in list")
        vfile = self._vfiles[name]
        vfile.edit(merge, **kwargs)

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
        self.guessit: dict = {}
        self.rules: list = []
        self.match: dict = {}
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
