from video_file_organizer.configs.config_handler \
    import ConfigHandler
import os


class FileSystemEntry:
    """
    The Object that takes care of the File System Entry in the Input Folder
    - path_to_fse: abspath path to fse
    """

    def __init__(self, config: ConfigHandler, item: str) -> None:
        self.config = config
        self.name = item

        self.abspath = os.path.join(config.input_dir, item)
        self.isdir = os.path.isdir(self.abspath)
        self.valid = False

        self.vfile = VideoFile()
        self._scan_fse()

    def _scan_fse(self):
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
                    if self.valid:
                        self.valid = False
                        break
                    self.vfile.filename = item
                    self.vfile.abspath = os.path.join(self.abspath, item)
                    self.valid = True

        else:
            # check if the file found has a valid file extension
            if self.config.re_file_ext_pattern.match(self.name):
                self.vfile.filename = self.name
                self.vfile.abspath = self.abspath
                self.valid = True


class VideoFile:
    def __init__(self):
        self.filename = None
        self.abspath = None
