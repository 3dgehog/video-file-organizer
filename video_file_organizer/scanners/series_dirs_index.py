import os
import logging


from video_file_organizer.configs.config_handler \
    import ConfigHandler


class SeriesDirsIndex:
    def __init__(self, config: ConfigHandler) -> None:
        self.series_dirs = config.series_dirs

        self.dict = self._scan_series_dirs()

    def _scan_series_dirs(self) -> dict:
        """sets self.series_dirs_index as
        {"foldername": {"path": "...", "subdirs": [..., ...]}} of all
        output folder in config.yaml"""
        logging.debug("indexing output directories")
        tempdict: dict = {}
        # List through listed output dirs
        for dir in self.series_dirs:
            dir = os.path.abspath(dir)

            # list through output dir
            for folder in os.listdir(dir):
                # Ignore not folders
                if not os.path.isdir(os.path.join(dir, folder)):
                    logging.debug("skipped '{}' because its not a \
                        directory".format(folder))
                    continue

                # Check incase duplicates found in series dirs
                if folder in tempdict:
                    raise KeyError("Duplicate name {}".format(folder))

                # Adds to path
                tempdict[folder] = {}
                tempdict[folder]['path'] = os.path.join(dir, folder)
                path = tempdict[folder]['path']

                # list though current dir to get subdir
                tempdict[folder]['subdirs'] = []
                for subfolder in os.listdir(path):
                    if not os.path.isdir(os.path.join(path, subfolder)):
                        continue

                    # Adds to subdir
                    tempdict[folder]['subdirs'].append(subfolder)
        logging.debug("indexing done")
        return tempdict
