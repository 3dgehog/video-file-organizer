import sys
import yaml
import subprocess
import shlex
import configparser
import os
import logging
import abc

from typing import Union, List, Optional
from jinja2 import Template

from video_file_organizer.utils import Observer
from video_file_organizer.entries import VideoFileEntry
from video_file_organizer.rules.utils import RuleRegistry

logger = logging.getLogger('vfo.config')

DEFAULT_DIR = '.config/video_file_organizer/'

CONFIG_FILE_TEMPLATE = """
# This is the main config file for video_file_organizer

# The directory it will search for the videos to sort
# *REQUIRED
# Example
# input_dir: "path/to/input/dir"
input_dir:

# List of directories it will copy the series to
# *REQUIRED
# Example
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
# Example
# before_scripts:
#   - "path/to/script"
before_scripts:


# list of scripts to run on_transfer.
# Example
# on_transfer:
#   - "path/to/script"
on_transfer:
"""

RULEBOOK_FILE_TEMPLATE = """
# series
# ---Pick 1 Only---
# season                     --> sets the transfer_to to the correct season
#                                folder
# parent-dir                 --> sets the transfer_to to the parent directory
# sub-dir "<subdir_name>"    --> sets the transfer_to to "<subdir_name>" in
#                                parent directory
# ------------------
# episode-only               --> Change season 1 episode 23 to episode 123
# format-title "<new_title>" --> Jinja formatting, variables are: episode,
#                                season, title, ...
#                                example: "One_Piece_{{ episode }}"
# alt-title                  --> Use the alternative title to search for file
#                                video

[series]
"""


class ConfigBase(metaclass=abc.ABCMeta):
    custom_path: Optional[str] = None
    default_filename: Optional[str] = None
    default_path: Optional[str] = None
    args: List[str]

    def load_args(self, args, **kwargs):
        return args

    def load_env(self, env, **kwargs):
        return env.split(':')

    @abc.abstractmethod
    def load_file(self, path: str, **kwargs) -> dict:
        pass

    def search_config(self, name: str, required: bool = False,
                      **kwargs) -> Union[list, None]:
        """Searches for config in 4 different places, args, env,
        a custom location & default location

        Args:
            name (str): The name of the config
            required (bool, optional): If this config is required. Defaults to
                False.

        Keyword Arguments:
            arg_name (str): Overwrites the default name for arguments
            env_name (str): Overwrites the default name for env variables
            file_name (str): Overwrites the default name for files

        Raises:
            ValueError: When the config couldn't be found and required is true

        Returns:
            list: It returns everything as a list
        """
        # args
        # returns list but doesn't change to string
        if self.args:
            args = self.load_args(self.args, name=name, **kwargs)
            if getattr(args, kwargs.get('arg_name') or name):
                return getattr(args, kwargs.get('arg_name') or name)

        # environment
        # returns a list and changes it to strings
        if os.environ.get(kwargs.get('env_name') or name.upper()):
            env = self.load_env(os.environ.get(
                kwargs.get('env_name') or name.upper(), **kwargs
            ))
            return env

        # custom file location
        if self.custom_path:
            file = self.load_file(self.custom_path, name=name, **kwargs)
            if file.get(kwargs.get('file_name') or name):
                return file.get(kwargs.get('file_name') or name)

        # default file locations
        if self.default_path:
            if os.path.exists(self.default_path):
                file = self.load_file(self.default_path)
                if file.get(kwargs.get('file_name') or name):
                    return file.get(kwargs.get('file_name') or name)

        # current directory
        if self.default_filename:
            if os.path.exists(self.default_filename):
                file = self.load_file(self.default_filename)
                if file.get(kwargs.get('file_name') or name):
                    return file.get(kwargs.get('file_name') or name)

        if required:
            raise ValueError(
                f"Couldn't find required config for {name.capitalize()}")
        return None


class Config(Observer, ConfigBase):
    default_filename = 'config.yaml'
    default_path = os.path.join(
        os.environ['HOME'],
        f'.config/video_file_organizer/{default_filename}'
    )

    def __init__(self, args):
        self.args = args

        self.custom_path = self.validate_custom_config_file(
            self.search_config('config_file')
        )

        self.input_dir = self.validate_input_dir(
            self.search_config('input_dir', required=True)
        )

        self.series_dirs = self.validate_series_dirs(
            self.search_config('series_dirs', required=True)
        )

        self.ignore = self.search_config('ignore')

        self.on_transfer_scripts = self.search_config(
            'on_transfer',
            arg_name='on_transfer_scripts'
        )

        self.schedule = self.validate_schedule(
            self.search_config('schedule')
        )

        self.run_before_scripts(self.search_config('before_scripts'))

        self.videoextensions = ['mkv', 'm4v', 'avi', 'mp4', 'mov']

    def validate_custom_config_file(
            self, path: Optional[List[str]]
    ) -> Optional[str]:
        if not path:
            return None

        if len(path) > 1:
            raise ValueError('More than 1 config file has been provided')

        if not os.path.exists(path[0]):
            raise FileNotFoundError(f"File {path[0]} doesn't exists")

        fileextension = path[0].rpartition('.')[-1]
        if fileextension not in ['yaml', 'yml']:
            raise TypeError('File needs to be a .yaml format')

        logger.debug(f"Got config file {path[0]}")
        return path[0]

    def validate_input_dir(self, path: Union[str, list]) -> str:
        if not isinstance(path, list):
            path = [path]

        if len(path) > 1:
            raise ValueError('More than 1 input dir has been provided')

        if not os.path.exists(path[0]):
            raise FileNotFoundError(f"File {path[0]} doesn't exists")

        logger.debug(f"Got input dir {path[0]}")
        return path[0]

    def validate_series_dirs(self, dirs: List[str]) -> list:
        for path in dirs:
            if not os.path.exists(path):
                raise FileNotFoundError(
                    f"Series Directory '{path}' doesn't exists")

        logger.debug(f"Got series dirs '{dirs}'")
        return dirs

    def validate_schedule(self, minutes: int):
        if isinstance(minutes, list):
            minutes = minutes[0]
        if isinstance(minutes, str):
            minutes = int(minutes)
        if not isinstance(minutes, int):
            raise ValueError('Schduler needs to be an integer')

        return minutes

    @staticmethod
    def create_file_from_template():
        """Creates config.yaml from template"""
        if os.path.exists('config.yaml'):
            logger.info("config.yaml already exists")
            return

        config_file = open('config.yaml', "w")
        config_file.write(CONFIG_FILE_TEMPLATE)
        config_file.close()

    def load_file(self, path: str, **kwargs) -> dict:
        if not os.path.exists(path):
            raise FileNotFoundError("Config file doesn't exist")

        with open(path, 'r') as yml:
            return yaml.load(yml, Loader=yaml.FullLoader)

    def run_before_scripts(self, scripts: Union[List[str], None]):
        if not scripts:
            logger.debug("No before scripts to run")
            return

        for script in scripts:
            logger.debug(f"Running before script '{script}'")
            self._run_script(script)
            logger.debug(f"Ran script {script}")

    def update(self, *args, topic: str, **kwargs):
        if topic == 'on_transfer':
            self.run_on_transfer_scripts(kwargs['vfile'])

    def run_on_transfer_scripts(self, vfile: VideoFileEntry):
        if not self.on_transfer_scripts:
            return
        for script in self.on_transfer_scripts:
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


class RuleBook(ConfigBase):
    default_filename = 'rule_book.ini'
    default_path = os.path.join(
        os.environ['HOME'],
        f'.config/video_file_organizer/{default_filename}'
    )

    def __init__(self, args):
        self.args = args

        self.custom_path = self.validate_custom_rule_book_file(
            self.search_config(
                'rule_book_file'
            )
        )

        self.all_series_rules = self.validate_series_rules(
            self.search_config(
                'series_rule',
                file_name='series',
                required=True
            )
        )

        self.list_of_series_name = self.all_series_rules.keys()

        self.rulebook_registry = RuleRegistry()

    def validate_custom_rule_book_file(
            self,
            path: List[str]
    ) -> Optional[str]:
        if not path:
            return None

        if len(path) > 1:
            raise ValueError('More than 1 rule book file has been provided')

        if not os.path.exists(path[0]):
            raise FileNotFoundError(f"File {path[0]} doesn't exists")

        fileextension = path[0].rpartition('.')[-1]
        if fileextension not in ['ini']:
            raise TypeError('File needs to be a .ini format')

        logger.debug(f"Got rule book file {path[0]}")
        return path[0]

    def validate_series_rules(
        self,
        series_rules_pairs: Union[dict, list]
    ) -> dict:
        series_dict: dict = {}
        if isinstance(series_rules_pairs, list):
            for pair in series_rules_pairs:
                title = pair[0]
                rules = pair[1:]
                series_dict[title] = rules
        elif isinstance(series_rules_pairs, dict):
            for title, rules in series_rules_pairs.items():
                series_dict[title] = shlex.split(rules)
        else:
            raise ValueError('Unknown type was passed')

        for title, rules in series_dict.items():
            self._validate_series_rules_pairs(rules)

        return series_dict

    def load_file(self, path: str, **kwargs) -> dict:
        config = configparser.ConfigParser(allow_no_value=True, dict_type=dict)
        config.read(path)
        return {s: dict(config.items(s)) for s in config.sections()}

    @staticmethod
    def create_file_from_template():
        """Creates rule_book.ini from template"""
        if os.path.exists('rule_book.ini'):
            logger.info("rule_book.ini already exists")
            return

        rulebook_file = open('rule_book.ini', "w")
        rulebook_file.write(RULEBOOK_FILE_TEMPLATE)
        rulebook_file.close()

    def get_series_rule_by_name(self, name: str) -> list:
        return self.all_series_rules.get(name)

    def _validate_series_rules_pairs(self, rules: list):
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
                    raise KeyError(f"Invalid series rule: '{rule}'")

        # Check invalid pairs
        for invalid_pair in INVALID_PAIRS:
            found = [rule for rule in rules if rule in invalid_pair]
            if len(found) > 1:
                raise KeyError(f"Invalid pair {found}")
