import pytest

from tests.vars import SERIES_CONFIGPARSE
from tests.utils import RuleBookFileInjector

from video_file_organizer.handlers.rule_book import RuleBookHandler


def test_invalid_rule(tmp_dir):
    rule_book_injector = RuleBookFileInjector(tmp_dir)
    rule_book_injector.configparse['series'] = {
        'That 70s Show': 'invalid-rule'
    }
    rule_book_injector.save()
    with pytest.raises(KeyError):
        RuleBookHandler(tmp_dir)


def test_valid_secondary_rule(tmp_dir):
    rule_book_injector = RuleBookFileInjector(tmp_dir)
    rule_book_injector.configparse['series'] = {
        'That 70s Show': 'sub-dir "hi"'
    }
    rule_book_injector.save()
    RuleBookHandler(tmp_dir)


def test_success_rulebookhandler(tmp_dir):
    rule_book_injector = RuleBookFileInjector(tmp_dir)
    rule_book_injector.configparse['series'] = SERIES_CONFIGPARSE
    rule_book_injector.save()
    RuleBookHandler(tmp_dir)
