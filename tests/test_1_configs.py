import pytest
import os
import subprocess

from tests.utils.vars import ASSETS_DIR

from tests.utils.injectors import ConfigInjector

from video_file_organizer.handlers.config import ConfigHandler
from video_file_organizer.app import App


def test_empty_config_folder(tmp_dir):
    """Test ValueError Exception on new empty config folder which indirectly
    tests:
    - Creation of new configs from templates
    - Opening and reading config.yaml
    - If all required fields are entered"""
    app = App()
    app.config_dir = tmp_dir
    # ValueError because the required fields are not entered
    with pytest.raises(ValueError):
        ConfigHandler(app)
    # Checks the files where created by the ConfigHandler
    assert os.path.exists(tmp_dir)


def test_none_existing_series_and_input_dirs(tmp_config_dir, tmp_dir):
    """Test ValueError on missing series_dirs and input_dir folders in path"""
    config_injector = ConfigInjector(tmp_config_dir)
    config_injector.append({
        "series_dirs": [os.path.join(tmp_dir, "series_dirs")],
        "input_dir": os.path.join(tmp_dir, "input_dir")
    })
    app = App()
    app.config_dir = tmp_config_dir
    # FileNotFoundError because the directory doesn't exist
    with pytest.raises(FileNotFoundError):
        ConfigHandler(app)


def test_failing_before_script(tmp_config_dir, tmp_dir):
    """Test if there is a fail before script"""
    config_injector = ConfigInjector(tmp_config_dir)
    os.mkdir(os.path.join(tmp_dir, "series_dirs"))
    os.mkdir(os.path.join(tmp_dir, "input_dir"))
    config_injector.append({
        "series_dirs": [os.path.join(tmp_dir, "series_dirs")],
        "input_dir": os.path.join(tmp_dir, "input_dir"),
        "before_scripts": [os.path.join(ASSETS_DIR, "fail_script.sh")]
    })
    app = App()
    app.config_dir = tmp_config_dir
    # CalledProcessError because the script failed
    with pytest.raises(subprocess.CalledProcessError):
        ConfigHandler(app)


def test_success_confighandler(tmp_config_dir, tmp_dir):
    config_injector = ConfigInjector(tmp_config_dir)
    os.mkdir(os.path.join(tmp_dir, "series_dirs"))
    os.mkdir(os.path.join(tmp_dir, "input_dir"))
    config_injector.append({
        "series_dirs": [os.path.join(tmp_dir, "series_dirs")],
        "input_dir": os.path.join(tmp_dir, "input_dir")
    })
    app = App()
    app.config_dir = tmp_config_dir
    ConfigHandler(app)
