import pytest
import os

from tests.vars import ASSETS_DIR

from tests.utils import ConfigFileInjector

from video_file_organizer.config import setup_config_dir
from video_file_organizer.config.config_file import ConfigFile


def test_invalid_path_var(tmp_dir):
    # TypeError because Configfile needs file with yaml extension
    with pytest.raises(TypeError):
        ConfigFile('tmp_dir')

    # FileNotFoundError because file doesn't exist
    with pytest.raises(FileNotFoundError):
        ConfigFile('test.yaml')

    # ValueError because required fields are not entered
    with pytest.raises(ValueError):
        ConfigFile(os.path.join(tmp_dir, 'config.yaml'), create=True)


def test_setup_config_dir(tmp_dir):
    setup_config_dir(tmp_dir)


def test_none_existing_series_and_input_dirs(tmp_dir):
    """Test ValueError on missing series_dirs and input_dir folders in path"""
    config_injector = ConfigFileInjector(tmp_dir)
    config_injector.append({
        "series_dirs": [os.path.join(tmp_dir, "series_dirs")],
        "input_dir": os.path.join(tmp_dir, "input_dir")
    })
    # FileNotFoundError because the directory doesn't exist
    with pytest.raises(FileNotFoundError):
        ConfigFile(config_injector.path)


def test_failing_before_script(tmp_dir):
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
        ConfigFile(config_injector.path)


def test_success_configfile(tmp_dir):
    """This is a test of if everything goes well"""
    config_injector = ConfigFileInjector(tmp_dir)
    os.mkdir(os.path.join(tmp_dir, "series_dirs"))
    os.mkdir(os.path.join(tmp_dir, "input_dir"))
    config_injector.append({
        "series_dirs": [os.path.join(tmp_dir, "series_dirs")],
        "input_dir": os.path.join(tmp_dir, "input_dir")
    })
    ConfigFile(config_injector.path)
