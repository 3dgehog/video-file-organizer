import shlex
import configparser
import os
import logging

from typing import Union, List, Optional

from .base import ConfigBase
from .vars import RULEBOOK_FILE_TEMPLATE

from video_file_organizer.rules.utils import RuleRegistry

logger = logging.getLogger('vfo.config')


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
