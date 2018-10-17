import os
import pytest
import tempfile
import yg.lockfile

from tests.utils.injectors import setup_app_with_injectors

from tests.fixtures.setup_assets import SERIES_CONFIGPARSE


def test_lockfile(tmp_config_dir, tmp_dir):
    app, config_injector, rule_book_injector = setup_app_with_injectors(
        tmp_config_dir)
    rule_book_injector.configparse['series'] = SERIES_CONFIGPARSE
    rule_book_injector.save()
    config_injector.append({
        "input_dir": tmp_dir,
        "series_dirs": [tmp_dir]
    })
    app.setup()
    with yg.lockfile.FileLock(
            os.path.join(tempfile.gettempdir(), 'vfo_lock'), timeout=10):
        with pytest.raises(yg.lockfile.FileLockTimeout):
            app.run()


# def test_transfer_event_rules_warning():
#     pass

def test_rules_final_results(tmp_config_dir,
                             extract_input_dir,
                             extract_series_dirs):
    app, config_injector, rule_book_injector = setup_app_with_injectors(
        tmp_config_dir)
    rule_book_injector.configparse['series'] = {
        "One Piece": 'sub-dir "One Piece Episodes" episode-only \
format-title "One_Piece_{{ episode }}"',
        "Mahoutsukai no Yome": 'parent-dir',
        "Brooklyn Nine Nine": 'season'
    }
    rule_book_injector.save()
    config_injector.append({
        "input_dir": extract_input_dir,
        "series_dirs": extract_series_dirs
    })
    app.setup()
    app.run()

    # Check if correct sub-dir, episode-only and format-title
    assert 'One_Piece_829.mkv' in os.listdir(
        os.path.join(extract_series_dirs[1],
                     "One Piece/One Piece Episodes/")
    )
    # Check if correct parent-dir
    assert '[HorribleSubs] Mahoutsukai no Yome - 24 [480p].mkv' in os.listdir(
        os.path.join(extract_series_dirs[1], "Mahoutsukai no Yome"))
    # Check if correct season folder
    assert 'Brooklyn.Nine-Nine.S05E13.HDTV.x264-SVA.mkv' in os.listdir(
        os.path.join(extract_series_dirs[0], 'Brooklyn 99/Season 5')
    )


def test_success_transferer(tmp_config_dir,
                            extract_input_dir,
                            extract_series_dirs):
    app, config_injector, rule_book_injector = setup_app_with_injectors(
        tmp_config_dir)
    rule_book_injector.configparse['series'] = SERIES_CONFIGPARSE
    rule_book_injector.save()
    config_injector.append({
        "input_dir": extract_input_dir,
        "series_dirs": extract_series_dirs
    })
    app.setup()
    app.run()
