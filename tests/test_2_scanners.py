from video_file_organizer.app import App
from video_file_organizer.scanners import scan_input_dir, scan_series_dirs

from tests.fixtures.setup import ASSET_RULES


def test_scan_input_dir(tmp_config_editor_populated):
    _, rule_editor, config_dir = tmp_config_editor_populated
    rule_editor(ASSET_RULES)
    app = App(config_dir=config_dir)
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


def test_scan_series_dirs(tmp_config_editor_populated):
    _, rule_editor, config_dir = tmp_config_editor_populated
    rule_editor(ASSET_RULES)
    app = App(config_dir=config_dir)
    series_index = scan_series_dirs(app)
    for name, entry in series_index.dict.items():
        # Check the name is the same from the entry
        assert name == entry.name
        # Check if all entries are included
        assert entry in series_index.entries
