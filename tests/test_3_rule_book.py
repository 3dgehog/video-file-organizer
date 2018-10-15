import pytest

from tests.fixtures.setup_assets import SERIES_CONFIGPARSE

from tests.utils.injectors import RuleBookInjector

from video_file_organizer.app import App
from video_file_organizer.events import EventHandler
from video_file_organizer.rules.rule_book import RuleBookHandler


def setup_app_for_rule_book(config_dir):
    """Returns an app instance and rule_book_editor. The app instance
    has the attr config_dir and event set"""
    app = App()
    app.config_dir = config_dir
    app.event = EventHandler(app)
    rule_book_editor = RuleBookInjector(config_dir)
    return app, rule_book_editor


def test_invalid_rule(tmp_config_dir):
    app, rule_book_injector = setup_app_for_rule_book(tmp_config_dir)
    rule_book_injector.configparse['series'] = {
        'That 70s Show': 'invalid-rule'
    }
    rule_book_injector.save()
    with pytest.raises(KeyError):
        RuleBookHandler(app)


def test_valid_secondary_rule(tmp_config_dir):
    app, rule_book_injector = setup_app_for_rule_book(tmp_config_dir)
    rule_book_injector.configparse['series'] = {
        'That 70s Show': 'sub-dir "hi"'
    }
    rule_book_injector.save()
    RuleBookHandler(app)


def test_missing_event(tmp_config_dir):
    app, rule_book_injector = setup_app_for_rule_book(tmp_config_dir)
    rule_book_injector.configparse['series'] = SERIES_CONFIGPARSE
    rule_book_injector.save()
    del app.event
    with pytest.raises(AttributeError):
        RuleBookHandler(app)


def test_success_rulebookhandler(tmp_config_dir):
    app, rule_book_injector = setup_app_for_rule_book(tmp_config_dir)
    rule_book_injector.configparse['series'] = SERIES_CONFIGPARSE
    rule_book_injector.save()
    RuleBookHandler(app)
