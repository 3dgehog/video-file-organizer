import os
import shutil
import subprocess
import logging
import yaml
import sys

from typing import List

logger = logging.getLogger('vfo.config_file')


CONFIG_FILE_TEMPLATE_LOCATION = os.path.join(
    os.path.dirname(__file__), 'config.yaml')


class ConfigFile:
    def __init__(
            self,
            path: str,
            create: bool = False) -> None:

        logger.debug("Initializing ConfigFile")

        self.path = path

        if create:
            self._create_config_file_yaml()

        fileextension = self.path.rpartition('.')[-1]
        if fileextension not in ['yaml', 'yml']:
            raise TypeError('File needs to be a yaml format')

        self.raw_config = self._get_config_file_yaml()

        self._validate_required_fields()
        self._run_before_scripts()

        self.input_dir = self._get_input_dir()
        self.series_dirs = self._get_series_dirs()
        self.ignore = self.raw_config["ignore"]

    def _create_config_file_yaml(self):
        """Creates config.yaml"""
        if os.path.exists(self.path):
            logger.info("config_file already exists")
            return
        shutil.copyfile(CONFIG_FILE_TEMPLATE_LOCATION, self.path)

    def _get_config_file_yaml(self) -> dict:
        """Return config.yaml as dict"""
        if not os.path.exists(self.path):
            raise FileNotFoundError("Config file doesn't exist")

        with open(self.path, 'r') as yml:
            return yaml.load(yml, Loader=yaml.FullLoader)

    def _validate_required_fields(self):
        """Validate all required fields"""
        required_fields = ["input_dir", "series_dirs"]
        for field in required_fields:
            if not self.raw_config[field]:
                raise ValueError(f"Value for '{field}' empty on config.yaml")
        logger.debug("All required fields are entered")

    def _run_before_scripts(self):
        """Run all before_scripts in config"""
        # Checks if there are scripts to run
        if not self.raw_config['before_scripts']:
            logger.debug("No before scripts to run")
            return
        # Run scripts
        for script in self.raw_config['before_scripts']:
            logger.debug("Running before script '{}'".format(script))
            try:
                subprocess.check_output([script], shell=True)
            except subprocess.CalledProcessError as e:
                logger.info(e)
                sys.exit()
            logger.debug("Ran script {}".format(script))

    def _get_input_dir(self) -> str:
        """Returns the input_dir path from the config.yaml"""
        # Checks that the directory exists
        if not os.path.exists(self.raw_config["input_dir"]):
            raise FileNotFoundError("File {} doesn't exists".format(
                self.raw_config["input_dir"]))

        logger.debug("Got input dir {}".format(
            self.raw_config["input_dir"]))
        return self.raw_config["input_dir"]

    def _get_series_dirs(self) -> list:
        """Returns list of all directories from config.yaml 'series_dirs'"""
        dirs: List[str] = []
        for dir_list in self.raw_config["series_dirs"]:
            # Checks that the directory exists
            if not os.path.exists(dir_list):
                raise FileNotFoundError(
                    "Series Directory '{}' doesn't exists".format(dirs))
            dirs.append(dir_list)

        logger.debug("Got series dirs '{}'".format(dirs))
        return dirs
