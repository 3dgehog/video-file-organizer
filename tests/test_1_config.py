import pytest
import os

from tests.vars import ASSETS_DIR, SERIES_CONFIGPARSE

from tests.utils import ConfigFileInjector, RuleBookFileInjector

from video_file_organizer.config import ConfigFile, RuleBookFile


def test_configfile(tmp_dir):
    # Missing create argument
    with pytest.raises(TypeError):
        ConfigFile('tmp_dir')

    # FileNotFoundError because Configfile file doesn't exists
    with pytest.raises(FileNotFoundError):
        ConfigFile('tmp_dir', False)

    # ValueError because required fields are not entered
    with pytest.raises(ValueError):
        ConfigFile(os.path.join(tmp_dir, 'config.yaml'), create=True)


def test_configfile_empty_folders(tmp_dir):
    """Test ValueError on missing series_dirs and input_dir folders in path"""
    config_injector = ConfigFileInjector(tmp_dir)
    config_injector.append({
        "series_dirs": [os.path.join(tmp_dir, "series_dirs")],
        "input_dir": os.path.join(tmp_dir, "input_dir")
    })
    # FileNotFoundError because the directory doesn't exist
    with pytest.raises(FileNotFoundError):
        ConfigFile(config_injector.path, False)


def test_configfile_failing_before_script(tmp_dir):
    """Test if there is a fail before script"""
    config_injector = ConfigFileInjector(tmp_dir)
    os.mkdir(os.path.join(tmp_dir, "series_dirs"))
    os.mkdir(os.path.join(tmp_dir, "input_dir"))
    config_injector.append({
        "series_dirs": [os.path.join(tmp_dir, "series_dirs")],
        "input_dir": os.path.join(tmp_dir, "input_dir"),
        "before_scripts": [os.path.join(ASSETS_DIR, "fail_script.sh")]
    })
    # CalledProcessError because the script failed
    with pytest.raises(SystemExit):
        ConfigFile(config_injector.path, False)


def test_success_configfile(tmp_dir):
    """This is a test of if everything goes well"""
    config_injector = ConfigFileInjector(tmp_dir)
    os.mkdir(os.path.join(tmp_dir, "series_dirs"))
    os.mkdir(os.path.join(tmp_dir, "input_dir"))
    config_injector.append({
        "series_dirs": [os.path.join(tmp_dir, "series_dirs")],
        "input_dir": os.path.join(tmp_dir, "input_dir")
    })
    ConfigFile(config_injector.path, False)


def test_rulebookfile():
    # Missing Arguments
    with pytest.raises(TypeError):
        RuleBookFile()

    # File doesn't exists
    with pytest.raises(FileNotFoundError):
        RuleBookFile('temp.ini', False)


def test_invalid_rule(tmp_dir):
    rule_book_injector = RuleBookFileInjector(tmp_dir)
    rule_book_injector.configparse['series'] = {
        'That 70s Show': 'invalid-rule'
    }
    rule_book_injector.save()
    with pytest.raises(KeyError):
        RuleBookFile(rule_book_injector.path, False)


def test_valid_secondary_rule_without_value(tmp_dir):
    rule_book_injector = RuleBookFileInjector(tmp_dir)
    rule_book_injector.configparse['series'] = {
        'That 70s Show': 'sub-dir'
    }
    rule_book_injector.save()
    RuleBookFile(rule_book_injector.path, False)


def test_valid_secondary_rule(tmp_dir):
    rule_book_injector = RuleBookFileInjector(tmp_dir)
    rule_book_injector.configparse['series'] = {
        'That 70s Show': 'sub-dir "hi"'
    }
    rule_book_injector.save()
    RuleBookFile(rule_book_injector.path, False)


def test_success_rulebookhandler(tmp_dir):
    rule_book_injector = RuleBookFileInjector(tmp_dir)
    rule_book_injector.configparse['series'] = SERIES_CONFIGPARSE
    rule_book_injector.save()
    RuleBookFile(rule_book_injector.path, False)
