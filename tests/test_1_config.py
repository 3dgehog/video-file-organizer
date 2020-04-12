import pytest
import os

from tests.vars import ASSETS_DIR

from tests.utils import ConfigFileInjector

from video_file_organizer.handlers.config import ConfigHandler


def test_empty_config_folder(tmp_dir):
    """Test ValueError Exception on new empty config folder which indirectly
    tests:
    - Creation of new configs from templates
    - Opening and reading config.yaml
    - If all required fields are entered"""
    # ValueError because the required fields are not entered
    with pytest.raises(FileNotFoundError):
        ConfigHandler(tmp_dir)

    with pytest.raises(ValueError):
        ConfigHandler(tmp_dir, create=True)
    # Checks the files where created by the ConfigHandler
    assert os.path.exists(tmp_dir)


def test_none_existing_series_and_input_dirs(tmp_dir):
    """Test ValueError on missing series_dirs and input_dir folders in path"""
    config_injector = ConfigFileInjector(tmp_dir)
    config_injector.append({
        "series_dirs": [os.path.join(tmp_dir, "series_dirs")],
        "input_dir": os.path.join(tmp_dir, "input_dir")
    })
    # FileNotFoundError because the directory doesn't exist
    with pytest.raises(FileNotFoundError):
        ConfigHandler(tmp_dir)


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
        ConfigHandler(tmp_dir)


def test_success_confighandler(tmp_dir):
    """This is a test of if everything goes well"""
    config_injector = ConfigFileInjector(tmp_dir)
    os.mkdir(os.path.join(tmp_dir, "series_dirs"))
    os.mkdir(os.path.join(tmp_dir, "input_dir"))
    config_injector.append({
        "series_dirs": [os.path.join(tmp_dir, "series_dirs")],
        "input_dir": os.path.join(tmp_dir, "input_dir")
    })
    ConfigHandler(tmp_dir)
