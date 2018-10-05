import os
import shutil
import subprocess
import logging
import yaml

CONFIG_DIR = os.path.join(os.environ['HOME'], '.config/video_file_organizer/')
CONFIG_TEMPLATES = os.path.join(os.path.dirname(__file__), 'config_templates')


class ConfigHandler:
    """Config Handler for the entire program"""

    def __init__(
            self, config_dir=CONFIG_DIR, config_templates=CONFIG_TEMPLATES):
        self.config_dir = config_dir
        self.config_templates = config_templates

        self._init_config_dir()
        self._config_yaml = self._get_config_yaml()
        self._run_before_scripts()
        self.series_dirs = self._get_series_dirs()
        self.ignore_folders = self._config_yaml["ignore_folders"]
        self.ignore_files = self._config_yaml["ignore_files"]
        self._rule_book_yaml = self._get_rule_book_yaml()

    def _init_config_dir(self):
        """Checks if ~/.config/video_file_organizer directory exists.
        If it doesn't it creates the directory and adds template config
        files inside"""
        if not os.path.exists(self.config_dir):
            logging.debug(
                "Config folder doesn't exists, therefore its created")
            os.makedirs(self.config_dir)

        for file in os.listdir(self.config_templates):
            if not os.path.exists(os.path.join(self.config_dir, file)):
                logging.debug(
                    "File '{}' wasn't in config directory \
                    therefore it was created".format(file))
                shutil.copyfile(
                    os.path.join(self.config_templates, file),
                    os.path.join(self.config_dir, file))

    def _get_config_yaml(self) -> dict:
        """Returns config.yaml as dict"""
        with open(os.path.join(self.config_dir, "config.yaml"), 'r') as yml:
            return yaml.load(yml)

    def _run_before_scripts(self):
        """Run all before_scripts in config.yaml"""
        if not self._config_yaml['before_scripts']:
            logging.debug("no before scripts to run")
            return
        for script in self._config_yaml['before_scripts']:
            logging.debug("running before script '{}'".format(script))
            subprocess.check_output([script], shell=True)
            logging.debug("script ran")

    def _get_series_dirs(self) -> list:
        """Returns list of all directories from config.yaml 'series_dirs'"""
        dirs: list = []
        if not self._config_yaml["series_dirs"]:
            raise ValueError(
                "You need to set at least one series_dirs in config.yaml")
        for dir_list in self._config_yaml["series_dirs"]:
            if not dir_list:
                raise ValueError(
                    "Couldn't find series directories from config.yaml")
            if not os.path.exists(dir_list):
                raise ValueError(
                    "Series Directory '{}' doesn't exists".format(dirs))
            dirs.append(dir_list)
        logging.debug("got series dirs '{}'".format(dirs))
        return dirs

    def _get_rule_book_yaml(self):
        """Returns rule_book.yaml file"""
        with open(os.path.join(self.config_dir, "rule_book.yaml"), 'r') as yml:
            return yaml.load(yml)
