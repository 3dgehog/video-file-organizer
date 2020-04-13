import sys
import yaml
import subprocess
import shutil
import shlex
import configparser
import os
import logging

from typing import Union, List

logger = logging.getLogger('vfo.config')

DEFAULT_DIR = '.config/video_file_organizer/'

CONFIG_FILE_TEMPLATE_LOCATION = os.path.join(
    os.path.dirname(__file__), 'config.yaml')


def setup_config_dir(
        path: Union[str, None],
        create: bool = False) -> str:

    if not path:
        path = os.path.join(os.environ['HOME'], DEFAULT_DIR)
        logger.debug(
            f'No config dir path given, going to default path of: {path}')

    if create:
        os.makedirs(path, exist_ok=True)
        logger.info("Config directory created")

    if not os.path.exists(path):
        raise FileNotFoundError("Config directory doesn't exist")

    return path


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


class RuleBookFile:
    def __init__(self, config_dir, setup=True) -> None:
        logger.debug("Initializing RuleBookHandler")
        self.config_dir = config_dir
        self.configparse = None

        if setup:
            self.setup()

    def setup(self):
        self.configparse = self._get_rule_book()
        self._validate_rule_book()

    def _get_rule_book(self):
        """Returns configparser object for rule_book.ini"""
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(os.path.join(self.config_dir, 'rule_book.ini'))
        return config

    def _validate_rule_book(self):
        """Checks if all the sections are valid and checks all the values of
        each entries"""
        # Validate sections
        RULE_BOOK_SECTIONS = ['series']
        for section in RULE_BOOK_SECTIONS:
            if not self.configparse.has_section(section):
                raise ValueError(f"Rule book has no {section} section")

        for section in self.configparse.sections():
            if section not in RULE_BOOK_SECTIONS:
                raise KeyError(f"Section '{section}' is not valid")

        # Validate series rules for all entries
        if self.configparse.has_section('series'):
            # Get all the options from series section
            for option in self.configparse.options('series'):
                # Get all the values for specific option
                rules = self.configparse.get('series', option)
                self._validate_series_rules(shlex.split(rules))
        logger.debug("Rule book was validated")

    def _validate_series_rules(self, rules: list):
        """Checks if all the rules from a specific entry has all valid options,
        doesn't have invalid pairs and that rules with secondary values are
        valid"""
        VALID_OPTIONS = [
            'season', 'parent-dir', 'sub-dir', 'episode-only', 'format-title',
            'alt-title', 'no-replace'
        ]
        INVALID_PAIRS = [['season', 'parent-dir', 'sub-dir']]
        RULES_WITH_SECONDARY = ['sub-dir', 'format-title']

        # Check if rules are valid
        for rule in rules:
            if rule not in VALID_OPTIONS:
                # Check wether its a value of a secondary value
                if rules[rules.index(rule) - 1] not in RULES_WITH_SECONDARY:
                    logger.critical("{}".format(rules))
                    raise KeyError("Invalid series rule: '{}'".format(rule))

        # Check invalid pairs
        for invalid_pair in INVALID_PAIRS:
            found = [rule for rule in rules if rule in invalid_pair]
            if len(found) > 1:
                raise KeyError("Invalid pair {}".format(found))
