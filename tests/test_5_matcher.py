import shutil
import os
import queue

from tests.utils.injectors import setup_app_with_injectors
from tests.utils.vars import SERIES_CONFIGPARSE

from video_file_organizer.scanners import scan_input_dir, scan_series_dirs
from video_file_organizer.matcher import matcher


def test_matcher_warnings(
        tmp_config_dir,
        extract_input_dir,
        extract_series_dirs,
        caplog):
    app, config_injector, rule_book_injector = setup_app_with_injectors(
        tmp_config_dir)
    rule_book_injector.configparse['series'] = SERIES_CONFIGPARSE
    rule_book_injector.save()
    config_injector.append({
        "input_dir": extract_input_dir,
        "series_dirs": extract_series_dirs
    })

    # Remove Supernatural Folder
    shutil.rmtree(os.path.join(extract_series_dirs[0], "Supernatural"))

    app.setup()
    app.series_index = scan_series_dirs(app.config.series_dirs)
    app.scan_queue = scan_input_dir(app.config, app.rule_book)

    # Set an FSE to an unknown type
    tmp_queue = queue.Queue()
    while True:
        if app.scan_queue.qsize() == 0:
            break
        fse = app.scan_queue.get()
        if fse.vfile.filename == "Arrow.S06E10.PROPER.HDTV.x264-CRAVERS.mkv":
            fse.type = "random"
        tmp_queue.put(fse)
    app.scan_queue = tmp_queue

    app.matched_queue = matcher(app.scan_queue, app.event, app.series_index)

    # Check if warning for missing Supernatural folder
    assert "FAILED MATCH: Unable to find a match: \
Supernatural.S13E15.HDTV.x264-KILLERS.mkv" \
        in caplog.text
    # Check if warning for unknown fse.type
    assert "FAILED INDEX: Unable to find index for type random: \
Arrow.S06E10.PROPER.HDTV.x264-CRAVERS.mkv" \
        in caplog.text


def test_match_event_rules_warning(tmp_config_dir,
                                   extract_input_dir,
                                   extract_series_dirs,
                                   caplog):
    app, config_injector, rule_book_injector = setup_app_with_injectors(
        tmp_config_dir)
    # Home NO SEASON FOLDER
    rule_book_injector.configparse['series'] = {
        "Homeland": 'season',
        "One Piece": 'sub-dir "null" episode-only',
        "Fresh of the Boat": 'season alt-title'
    }
    rule_book_injector.save()
    config_injector.append({
        "input_dir": extract_input_dir,
        "series_dirs": extract_series_dirs
    })
    app.setup()
    app.series_index = scan_series_dirs(app.config.series_dirs)
    app.scan_queue = scan_input_dir(app.config, app.rule_book)
    app.matched_queue = matcher(app.scan_queue, app.event, app.series_index)

    # Created the missing season folder for Homeland
    assert "SEASON RULE: Created new Season 7 \
folder for Series Homeland" in caplog.text
    # One Piece doesn't have sub-dir 'null'
    assert "FAILED SUB-DIR RULE: Cannot locate sub-dir null: \
[HorribleSubs] One Piece - 829 [720p].mkv" in caplog.text
    # Fresh of the Boat doesn't have an alt-title
    assert "FAILED ALT-TITLE RULE: Alternative title missing: \
Fresh.Off.the.Boat.S04E14.WEBRip.x264-ION10.mp4" in caplog.text


def test_success_matcher(
        tmp_config_dir, extract_input_dir, extract_series_dirs):
    app, config_injector, rule_book_injector = setup_app_with_injectors(
        tmp_config_dir)
    rule_book_injector.configparse['series'] = SERIES_CONFIGPARSE
    rule_book_injector.save()
    config_injector.append({
        "input_dir": extract_input_dir,
        "series_dirs": extract_series_dirs
    })
    app.setup()
    app.series_index = scan_series_dirs(app.config.series_dirs)
    app.scan_queue = scan_input_dir(app.config, app.rule_book)
    app.matched_queue = matcher(app.scan_queue, app.event, app.series_index)

    while True:
        if app.matched_queue.qsize() == 0:
            break

        fse = app.matched_queue.get()

        # Check that all fse have all matched variables
        assert fse.matched_dir_path is not None
        assert fse.matched_dir_name is not None
        assert fse.matched_dir_entry is not None
