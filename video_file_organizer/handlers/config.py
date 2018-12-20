import os
import shutil
import subprocess
import logging
import yaml
import re
from typing import Pattern


logger = logging.getLogger('app.config')

CONFIG_TEMPLATES = os.path.join(
    os.path.dirname(__file__), '../config_templates')
VIDEO_EXTENSIONS = ['mkv', 'm4v', 'avi', 'mp4', 'mov']


class ConfigHandler:
    """The ConfigHandler handles all the configs of the application and is a
    layer between the application and the config.yaml file. """

    def __init__(self, app) -> None:
        logger.debug("Initializing ConfigHandler")
        app._requirements(['config_dir'])
        self.app = app
        self.config_dir = app.config_dir
        self.config_templates = CONFIG_TEMPLATES

        self._init_config_dir()
        self._config_yaml = self._get_config_yaml()
        self._check_required_fields()
        self._run_before_scripts()
        self.input_dir = self._get_input_dir()
        self.series_dirs = self._get_series_dirs()
        self.ignore = self._config_yaml["ignore"]
        self.re_file_ext_pattern = self._compile_video_file_ext_pattern()

        self.args = None

    def _init_config_dir(self):
        """Checks if ~/.config/video_file_organizer directory exists.
        If it doesn't it creates the directory and adds template config
        files inside"""
        if not os.path.exists(self.config_dir):
            logger.debug("Config folder doesn't exists, therefore its created")
            os.makedirs(self.config_dir)

        for file in os.listdir(self.config_templates):
            if not os.path.exists(os.path.join(self.config_dir, file)):
                logger.debug("File '{}' wasn't in ".format(file) +
                             "config directory therefore it was created")
                shutil.copyfile(
                    os.path.join(self.config_templates, file),
                    os.path.join(self.config_dir, file))

    def _get_config_yaml(self) -> dict:
        """Returns config.yaml as dict"""
        with open(os.path.join(self.config_dir, "config.yaml"), 'r') as yml:
            return yaml.load(yml)

    def _check_required_fields(self):
        """Checks that all the required fields are not empty"""
        required_fields = [
            "input_dir",
            "series_dirs"
        ]
        for field in required_fields:
            if not self._config_yaml[field]:
                raise ValueError(
                    "Value for '{}' empty on config.yaml".format(field))
        logger.debug("all required fields are entered")

    def _run_before_scripts(self):
        """Run all before_scripts in config.yaml"""
        # Checks if there are scripts to run
        if not self._config_yaml['before_scripts']:
            logger.debug("no before scripts to run")
            return
        # Run scripts
        for script in self._config_yaml['before_scripts']:
            logger.debug("running before script '{}'".format(script))
            subprocess.check_output([script], shell=True)
            logger.debug("script ran")

    def _get_input_dir(self) -> str:
        """Returns the input_dir path from the config.yaml"""
        # Checks that the directory exists
        if not os.path.exists(self._config_yaml["input_dir"]):
            raise FileNotFoundError("{} doesn't exists".format(
                self._config_yaml["input_dir"]))

        logger.debug("got input dir {}".format(
            self._config_yaml["input_dir"]))
        return self._config_yaml["input_dir"]

    def _get_series_dirs(self) -> list:
        """Returns list of all directories from config.yaml 'series_dirs'"""
        dirs: list = []
        for dir_list in self._config_yaml["series_dirs"]:
            # Checks that the directory exists
            if not os.path.exists(dir_list):
                raise FileNotFoundError(
                    "Series Directory '{}' doesn't exists".format(dirs))
            dirs.append(dir_list)

        logger.debug("got series dirs '{}'".format(dirs))
        return dirs

    def _compile_video_file_ext_pattern(self) -> Pattern[str]:
        """returns re.compile('^.*(\.mkv|\.mp4)$', re.IGNORECASE)"""
        extensions = VIDEO_EXTENSIONS
        output = '^.*('
        for extension in extensions:
            output = output + '\.' + extension + '|'
        output = output[:-1] + ")$"
        return re.compile("{}".format(output), re.IGNORECASE)
