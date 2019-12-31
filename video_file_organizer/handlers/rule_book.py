import configparser
import os
import difflib
import shlex
import logging

from video_file_organizer.models import VideoFile

logger = logging.getLogger('vfo.rule_book')


class RuleBookHandler:
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

    def get_vfile_rules(self, vfile: VideoFile):
        if not isinstance(vfile, VideoFile):
            raise TypeError("vfile needs to be an instance of VideoFile")
        if not hasattr(vfile, 'guessit'):
            raise AttributeError("Guessit attribute missing")

        name = vfile.name
        vtype = vfile.guessit['type']
        title = vfile.guessit['title']
        alternative_title = None
        if 'alternative_title' in vfile.guessit:
            alternative_title = vfile.guessit['alternative_title']

        return self.get_rules(name, vtype, title, alternative_title)

    def get_rules(
            self, name: str, vtype: str, title: str,
            alternative_title: str = None):
        VALID_TYPES = {"episode": self._get_series_rules}

        rules = []
        for key, func in VALID_TYPES.items():
            if vtype == key:
                rules = func(name, title, alternative_title)

        if len(rules) == 0:
            logger.warn(f"Unable to find the rules for: {name}")
            return None

        return rules

    def _get_series_rules(self, name, title=None, alternative_title=None):
        """Uses the title from the fse to try to match to its rules type from the
        rule_book.ini"""
        if title is None:
            return []

        # Get difflib_match from title
        DIFF_CUTOFF = 0.7
        difflib_match = difflib.get_close_matches(
            title, self.configparse.options('series'),
            n=1, cutoff=DIFF_CUTOFF)

        # Get difflib_match from alternative_title
        if not difflib_match and alternative_title:
            difflib_match = difflib.get_close_matches(
                ' '.join([title, alternative_title]),
                self.configparse.options('series'),
                n=1, cutoff=DIFF_CUTOFF
            )

        # Get the rules from the rule_book with difflib_match
        rules = []
        if difflib_match:
            rules = shlex.split(self.configparse.get(
                'series', difflib_match[0]))

        return rules
