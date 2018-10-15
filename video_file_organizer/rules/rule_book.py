import configparser
import os
import difflib
import importlib
import shlex

VALID_SECTIONS = ['series']


class RuleBookHandler:
    def __init__(self, app) -> None:
        app._requirements(['config_dir', 'event'])
        self.app = app
        self.config_dir = app.config_dir
        self.configparse = self._get_rule_book()
        self._check_rule_book()
        self._validate_rule_book()
        self._set_event_listeners()

    def _get_rule_book(self):
        """Returns configparser object for rule_book.ini"""
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(os.path.join(self.config_dir, 'rule_book.ini'))
        return config

    def _check_rule_book(self):
        """Simple check to see if the rule_book has the section series"""
        if not self.configparse.has_section('series'):
            raise ValueError("Rule book is empty")

    def _validate_rule_book(self):
        """Checks if all the sections are valid and checks all the values of
        each entries"""
        # Validates all sections
        for section in self.configparse.sections():
            if section not in VALID_SECTIONS:
                raise KeyError("Section '{}' is not valid".format(section))

        # Validate series rules for all entries
        if self.configparse.has_section('series'):
            # Get all the options from series section
            for option in self.configparse.options('series'):
                # Get all the values for specific option
                rules = self.configparse.get('series', option)
                self._validate_series_rules_values(shlex.split(rules))

    def _validate_series_rules_values(self, rules: list):
        """Checks if all the rules from a specific entry has all valid options,
        doesn't have invalid pairs and that rules with secondary values are 
        valid"""
        VALID_OPTIONS = ['season', 'parent-dir', 'sub-dir']
        INVALID_PAIRS = [['season', 'parent-dir', 'sub-dir']]
        RULES_WITH_SECONDARY = ['sub-dir']
        for rule in rules:
            if rule not in VALID_OPTIONS:
                # Check wether its a value of a secondary rule
                for secondary_rule in RULES_WITH_SECONDARY:
                    if not rules[rules.index(rule) - 1] != secondary_rule:
                        continue
                    raise KeyError("Invalid series rule: '{}'".format(rule))
        # Check invalid pairs
        for invalid_pair in INVALID_PAIRS:
            found = [rule for rule in rules if rule in invalid_pair]
            if len(found) > 1:
                raise KeyError("Invalid pair {}".format(found))

    def _set_event_listeners(self):
        # Add event listeners for the series category
        series = importlib.import_module('video_file_organizer.rules.series')
        for rule in [x for x in dir(series) if 'rule_' in x]:
            func = getattr(series, rule)
            for event, listener in self.app.event.event_list.items():
                if event in func.event:
                    listener(func)

    def get_series_rules_by_title(self, title: str) -> list:
        rules: list = []
        DIFF_CUTOFF = 0.7
        difflib_match = difflib.get_close_matches(
            title, self.configparse.options('series'), n=1, cutoff=DIFF_CUTOFF)
        if difflib_match:
            rules = shlex.split(self.configparse.get(
                'series', difflib_match[0]))
        return rules
