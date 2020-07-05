import sys
import yaml
import subprocess
import shlex
import configparser
import os
import logging

from typing import Union, List
from jinja2 import Template

from video_file_organizer.utils import Observer
from video_file_organizer.models import VideoFile

logger = logging.getLogger('vfo.config')

DEFAULT_DIR = '.config/video_file_organizer/'

CONFIG_FILE_TEMPLATE_LOCATION = os.path.join(
    os.path.dirname(__file__), 'config.yaml')
RULEBOOK_FILE_TEMPLATE_LOCATION = os.path.join(
    os.path.dirname(__file__), 'rule_book.ini')

CONFIG_FILE_TEMPLATE = """
# This is the main config file for video_file_organizer

# The directory it will search for the videos to sort
# REQUIRED
# Example
# input_dir: "path/to/input/dir"
input_dir:

# List of directories it will copy the series to
# REQUIRED
# Example.
# output_dirs:
#   - path/to/dir/1
series_dirs:

# List of files and folders to ignore from input_dir
# Example
# ignore:
#   - ".stversions"
ignore:

# Advanced Options

# list of scripts to run before starting.
# Especially useful if your folders are located on a network drive that you
# need to mount first
# Example:
# before_scripts:
#   - "path/to/script"
before_scripts:


# list of scripts to run on_transfer.
# Example:
# on_transfer:
#   - "path/to/script"
on_transfer:
"""

RULEBOOK_FILE_TEMPLATE = """
## series
# ---Pick 1 Only---
# season --> sets the transfer_to to the correct season folder
# parent-dir --> sets the transfer_to to the parent directory
# sub-dir "<subdir_name>" --> sets the transfer_to to "<subdir_name>" in
#   parent directory
# -----------------
# episode-only --> Change season 1 episode 23 to episode 123
# format-title "<new_title>" --> Jinja formatting, variables are: episode,
#   season, title, ... example: "One_Piece_{{ episode }}"
# alt-title --> Use the alternative title to search for file video

[series]
"""


class ConfigDirectory:
    def __init__(self, path: Union[str, None] = None):
        # Default path if path not provided
        if not path:
            path = os.path.join(os.environ['HOME'], DEFAULT_DIR)
            logger.debug('No config dir path given, going to default'
                         f' path of: {path}')

        self.path = path

        # Create if it doesn't exists
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            logger.info("Config directory created")

        # Initiate file handlers
        self.configfile = ConfigFile(
            os.path.join(self.path, 'config.yaml'),
        )
        self.rulebookfile = RuleBookFile(
            os.path.join(self.path, 'rule_book.ini'),
        )


class ConfigFile(Observer):
    VALID_OPTIONS = ['input_dir', 'series_dirs',
                     'ignore', 'before_scripts', 'on_transfer']

    def __init__(self, path: str):

        logger.debug("Initializing ConfigFile")

        self.path = path

        if not os.path.exists(path):
            self.create_file_from_template()

        fileextension = self.path.rpartition('.')[-1]
        if fileextension not in ['yaml', 'yml']:
            raise TypeError('File needs to be a .yaml format')

        self._raw_config = self.load_file()

        self.validate()
        self.run_before_scripts()

        self.input_dir = self.get_input_dir()
        self.series_dirs = self.get_series_dirs()
        self.ignore = self._raw_config["ignore"]
        self.videoextensions = ['mkv', 'm4v', 'avi', 'mp4', 'mov']

    def get_input_dir(self) -> str:
        """Returns the input_dir path from the config.yaml"""
        # Checks that the directory exists
        if not os.path.exists(self._raw_config["input_dir"]):
            raise FileNotFoundError("File {} doesn't exists".format(
                self._raw_config["input_dir"]))

        logger.debug("Got input dir {}".format(
            self._raw_config["input_dir"]))
        return self._raw_config["input_dir"]

    def get_series_dirs(self) -> list:
        """Returns list of all directories from config.yaml 'series_dirs'"""
        dirs: List[str] = []
        for dir_list in self._raw_config["series_dirs"]:
            # Checks that the directory exists
            if not os.path.exists(dir_list):
                raise FileNotFoundError(
                    "Series Directory '{}' doesn't exists".format(dirs))
            dirs.append(dir_list)

        logger.debug("Got series dirs '{}'".format(dirs))
        return dirs

    def create_file_from_template(self):
        """Creates config.yaml from template"""
        if os.path.exists(self.path):
            logger.info("config.yaml already exists")
            return

        config_file = open(self.path, "w")
        config_file.write(CONFIG_FILE_TEMPLATE)
        config_file.close()

    def load_file(self) -> dict:
        """Return config.yaml as dict"""
        if not os.path.exists(self.path):
            raise FileNotFoundError("Config file doesn't exist")

        with open(self.path, 'r') as yml:
            return yaml.load(yml, Loader=yaml.FullLoader)

    def validate(self):
        """Validate all required fields"""
        for option in self._raw_config:
            if option not in self.VALID_OPTIONS:
                raise ValueError(f'{option} is not a valid option')

        required_fields = ["input_dir", "series_dirs"]
        for field in required_fields:
            if not self._raw_config[field]:
                raise ValueError(f"Value for '{field}' empty on config.yaml")
        logger.debug("All required fields are entered")

    def run_before_scripts(self):
        """Run all before_scripts in config"""
        # Checks if there are scripts to run
        if not self._raw_config['before_scripts']:
            logger.debug("No before scripts to run")
            return
        # Run scripts
        for script in self._raw_config['before_scripts']:
            logger.debug("Running before script '{}'".format(script))
            self._run_script(script)
            logger.debug("Ran script {}".format(script))

    def update(self, *args, topic: str, **kwargs):
        if topic == 'on_transfer':
            self.run_on_transfer_scripts(kwargs['vfile'])

    def run_on_transfer_scripts(self, vfile: VideoFile):
        if not self._raw_config['on_transfer']:
            return
        for script in self._raw_config['on_transfer']:
            logger.debug(f"Running on_transfer for vfile: '{vfile.name}'")
            values: dict = {}
            values.update(vars(vfile))
            values.update(vars(vfile)['metadata'])
            rendered_script = Template(script).render(values)
            self._run_script(rendered_script)

    def _run_script(self, script: str):
        try:
            subprocess.run([script], shell=True, check=True)
        except subprocess.CalledProcessError as e:
            logger.info(e)
            sys.exit()


class RuleBookFile:
    def __init__(self, path: str):
        logger.debug("Initializing RuleBookFile")

        self.path = path

        if not os.path.exists(path):
            self.create_file_from_template()

        fileextension = self.path.rpartition('.')[-1]
        if fileextension not in ['ini']:
            raise TypeError('File needs to be a .ini format')

        self.configparse = self.load_file()
        self.validate_rule_book()

    def load_file(self) -> configparser.ConfigParser:
        """Returns configparser object for rule_book.ini"""
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(self.path)
        return config

    def create_file_from_template(self):
        """Creates rule_book.ini from template"""
        if os.path.exists(self.path):
            logger.info("rule_book.ini already exists")
            return

        rulebook_file = open(self.path, "w")
        rulebook_file.write(RULEBOOK_FILE_TEMPLATE)
        rulebook_file.close()

    def list_of_series(self):
        return self.configparse.options('series')

    def get_series_rule(self, name: str) -> str:
        return self.configparse.get('series', name)

    def validate_rule_book(self):
        """Checks if all the sections are valid and checks all the values of
        each entries"""
        # Validate sections
        RULE_BOOK_SECTIONS = ['series']

        for section in RULE_BOOK_SECTIONS:
            if not self.configparse.has_section(section):
                raise ValueError(f"Rule book is missing {section} section")

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
                    logger.critical(f"{rules}")
                    raise KeyError("Invalid series rule: '{}'".format(rule))

        # Check invalid pairs
        for invalid_pair in INVALID_PAIRS:
            found = [rule for rule in rules if rule in invalid_pair]
            if len(found) > 1:
                raise KeyError(f"Invalid pair {found}")
