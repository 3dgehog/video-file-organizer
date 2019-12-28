import configparser
import os
import difflib
import importlib
import shlex
import logging

from video_file_organizer.settings import VALID_SECTIONS


logger = logging.getLogger('app.rule_book')


class RuleBookHandler:
    def __init__(self, config_dir, event) -> None:
        logger.debug("Initializing RuleBookHandler")
        self.config_dir = config_dir
        self.event = event
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
            raise ValueError("Rule book has no series section")

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
        logger.debug("Rule book was validated")

    def _validate_series_rules_values(self, rules: list):
        """Checks if all the rules from a specific entry has all valid options,
        doesn't have invalid pairs and that rules with secondary values are
        valid"""
        VALID_OPTIONS = [
            'season', 'parent-dir', 'sub-dir', 'episode-only', 'format-title',
            'alt-title', 'no-replace'
        ]
        INVALID_PAIRS = [['season', 'parent-dir', 'sub-dir']]
        RULES_WITH_SECONDARY = ['sub-dir', 'format-title']
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

    def _set_event_listeners(self):
        """ Add event listeners for the series category in order"""
        series = importlib.import_module('video_file_organizer.rules.series')
        # Loops thru a list of all functions that start with 'rule_'
        for rule in [x for x in dir(series) if 'rule_' in x]:
            # Gets the function using getattr()
            rule_func = getattr(series, rule)
            # Loops thru all the events and their listeners
            for event, listener in self.event.event_listeners_list.items():
                rule_list = []
                # Loops thru all the events the rule_func has
                for set_event, set_order in rule_func.events:
                    if set_event == event:
                        rule_list.append((set_event, set_order))
                # Sorts by the order from the function attr
                rule_list.sort(key=lambda x: x[1])
                for set_event, set_order in rule_list:
                    listener(rule_func)
                    logger.debug("Added rule function {} to event {}".format(
                        rule_func.__name__, set_event))

    def get_fse_rules(self, fse) -> list:
        """Uses the video type to get all the rules from that specific type"""
        VALID_TYPES = {
            "episode": self._get_series_rules
        }
        rules = []
        for key, func in VALID_TYPES.items():
            if fse.type == key:
                rules = func(fse, rules)

        if len(rules) == 0:
            logger.log(11, "NO RULE MATCHED: " +
                       "Unable to find the rules for: " +
                       "{}".format(fse.vfile.filename))
            fse.valid = False

        return rules

    def _get_series_rules(self, fse, rules):
        """Uses the title from the fse to try to match to its rules type from the
        rule_book.ini"""
        DIFF_CUTOFF = 0.7
        difflib_match = difflib.get_close_matches(
            fse.title, self.configparse.options('series'),
            n=1, cutoff=DIFF_CUTOFF)

        # Check if there is an alternative title and tries to use it also
        if not difflib_match and 'alternative_title' in fse.details:
            difflib_match = difflib.get_close_matches(
                ' '.join(
                    [fse.details['title'], fse.details['alternative_title']]
                ), self.configparse.options('series'), n=1, cutoff=DIFF_CUTOFF
            )

        # Get the rules from the rule_book
        if difflib_match:
            rules = shlex.split(self.configparse.get(
                'series', difflib_match[0]))

        return rules
