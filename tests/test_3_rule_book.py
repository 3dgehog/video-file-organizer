import pytest

from tests.fixtures.setup_assets import App
from tests.fixtures.setup_3_rule_book \
    import TESTRuleBookEditor, SERIES_CONFIGPARSE

from video_file_organizer.events import EventHandler
from video_file_organizer.rules.rule_book import RuleBookHandler


def test_invalid_rule(config_editor):
    config_editor, config_dir = config_editor
    app = App()
    app.config_dir = config_dir
    app.event = EventHandler(app)
    rule_book = TESTRuleBookEditor(config_dir)
    rule_book.configparse['series'] = {'That 70s Show': 'invalid-rule'}
    rule_book.save()
    with pytest.raises(KeyError):
        RuleBookHandler(app)


def test_valid_secondary_rule(config_editor):
    config_editor, config_dir = config_editor
    app = App()
    app.config_dir = config_dir
    app.event = EventHandler(app)
    rule_book = TESTRuleBookEditor(config_dir)
    rule_book.configparse['series'] = {'That 70s Show': 'sub-dir "hi"'}
    rule_book.save()
    RuleBookHandler(app)


def test_missing_event(config_editor):
    config_editor, config_dir = config_editor
    app = App()
    app.config_dir = config_dir
    rule_book = TESTRuleBookEditor(config_dir)
    rule_book.configparse['series'] = SERIES_CONFIGPARSE
    rule_book.save()
    with pytest.raises(AttributeError):
        RuleBookHandler(app)


def test_success_rulebookhandler(config_editor):
    config_editor, config_dir = config_editor
    app = App()
    app.config_dir = config_dir
    app.event = EventHandler(app)
    rule_book = TESTRuleBookEditor(config_dir)
    rule_book.configparse['series'] = SERIES_CONFIGPARSE
    rule_book.save()
    RuleBookHandler(app)
