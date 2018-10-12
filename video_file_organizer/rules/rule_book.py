import yaml
import os
import difflib
from typing import Union

VALID_CATEGORIES = ['Series']
VALID_SERIES_RULES = ['type', 'sub-dir']


class RuleBookHandler:
    def __init__(self, app) -> None:
        self.app = app
        self.config_dir = app.config.config_dir
        self.rule_book_dict = self._get_rule_book_yaml()
        self._check_rule_book()
        self._validate_rules()

    def _get_rule_book_yaml(self):
        """Returns rule_book.yaml file"""
        with open(os.path.join(self.config_dir, "rule_book.yaml"), 'r') as yml:
            return yaml.load(yml)

    def _check_rule_book(self):
        if not self.rule_book_dict['Series']:
            raise ValueError("Rule book is empty")

    def get_series_rules_by_title(self, title: str) -> Union[str, None]:
        rules = None
        DIFF_CUTOFF = 0.7
        diffmatch = difflib.get_close_matches(
            title, self.rule_book_dict['Series'], n=1, cutoff=DIFF_CUTOFF)
        if diffmatch:
            rules = self.rule_book_dict['Series'][diffmatch[0]]
        return rules

    def _validate_rules(self):
        # Validate categories
        for category, category_options in self.rule_book_dict.items():
            if category not in VALID_CATEGORIES:
                raise KeyError("Category '{}' is not valid".format(category))

            # Check Series Rules
            if category == "Series":
                for series_title, rules in category_options.items():
                    for rule, value in rules.items():
                        if rule not in VALID_SERIES_RULES:
                            raise KeyError(
                                "Rule '{}' is not valid in 'Series' category ",
                                "from series titled '{}'".format(
                                    category, series_title))
