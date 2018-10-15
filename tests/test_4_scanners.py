from tests.fixtures.setup_assets import SERIES_CONFIGPARSE

from tests.utils.injectors import ConfigInjector, RuleBookInjector

from video_file_organizer.app import App
from video_file_organizer.configs import ConfigHandler
from video_file_organizer.events import EventHandler
from video_file_organizer.rules.rule_book import RuleBookHandler
from video_file_organizer.scanners import scan_input_dir, scan_series_dirs


def setup_app_for_scanners(config_dir):
    """Returns app object and rule_book_injector. app has the attr
    config_dir and event"""
    app = App()
    app.config_dir = config_dir
    config_injector = ConfigInjector(config_dir)
    app.event = EventHandler(app)
    rule_book_injector = RuleBookInjector(config_dir)
    return app, config_injector, rule_book_injector


def test_scan_input_dir(tmp_config_dir, extract_input_dir, tmp_dir):
    input_dir = extract_input_dir
    series_dirs = [tmp_dir]
    app, config_injector, rule_book_injector = setup_app_for_scanners(
        tmp_config_dir)
    rule_book_injector.configparse['series'] = SERIES_CONFIGPARSE
    rule_book_injector.save()
    config_injector.append({
        "input_dir": input_dir,
        "series_dirs": series_dirs
    })
    app.config = ConfigHandler(app)
    app.rule_book = RuleBookHandler(app)
    app.scan_queue = scan_input_dir(app)
    while True:
        if app.scan_queue.qsize() == 0:
            break

        fse = app.scan_queue.get()

        # Check if all fse in queue are valid
        assert fse.valid is True
        # Check if all fse have found their video file
        assert fse.vfile.filename is not None
        # Check if all fse have found their video file abspath
        assert fse.vfile.abspath is not None
        # Check if all fse have titles
        assert fse.title is not None
        # Check if all fse have a type
        assert fse.type is not None
        # Check if all fse have rules
        assert fse.rules is not None


def test_scan_series_dirs(tmp_config_dir, extract_series_dirs, tmp_dir):
    input_dir = tmp_dir
    series_dirs = extract_series_dirs
    app, config_injector, rule_book_injector = setup_app_for_scanners(
        tmp_config_dir)
    rule_book_injector.configparse['series'] = SERIES_CONFIGPARSE
    rule_book_injector.save()
    config_injector.append({
        "input_dir": input_dir,
        "series_dirs": series_dirs
    })
    app.config = ConfigHandler(app)
    app.rule_book = RuleBookHandler(app)
    app.series_index = scan_series_dirs(app)
    for name, entry in app.series_index.dict.items():
        # Check the name is the same from the entry
        assert name == entry.name
        # Check if all entries are included
        assert entry in app.series_index.entries
