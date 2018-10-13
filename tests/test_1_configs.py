import pytest
import os
import subprocess

from tests.fixtures.setup_assets import App, ASSETS_DIR
from tests.fixtures.setup_1_configs import CONFIG_DIR

from video_file_organizer.configs import ConfigHandler


def test_empty_config_folder(tmp_dir):
    """Test ValueError Exception on new empty config folder which indirectly
    tests:
    - Creation of new configs from templates
    - Opening and reading config.yaml
    - If all required fields are entered"""
    config_dir = os.path.join(tmp_dir, CONFIG_DIR)
    app = App()
    app.config_dir = config_dir
    # ValueError because the required fields are not entered
    with pytest.raises(ValueError):
        ConfigHandler(app)
    # Checks the files where created by the ConfigHandler
    assert os.path.exists(config_dir)


def test_none_existing_series_and_input_dirs(config_editor, tmp_dir):
    """Test ValueError on missing series_dirs and input_dir folders in path"""
    config_editor, config_dir = config_editor
    config_editor({
        "series_dirs": [os.path.join(config_dir, "series_dirs")],
        "input_dir": os.path.join(tmp_dir, "input_dir")
    })
    app = App()
    app.config_dir = config_dir
    # FileNoteFoundError because the directory doesn't exist
    with pytest.raises(FileNotFoundError):
        ConfigHandler(app)


def test_failing_before_script(config_editor, tmp_dir):
    """Test if there is a fail before script"""
    config_editor, config_dir = config_editor
    os.mkdir(os.path.join(tmp_dir, "series_dirs"))
    os.mkdir(os.path.join(tmp_dir, "input_dir"))
    config_editor({
        "series_dirs": [os.path.join(tmp_dir, "series_dirs")],
        "input_dir": os.path.join(tmp_dir, "input_dir"),
        "before_scripts": [os.path.join(ASSETS_DIR, "fail_script.sh")]
    })
    app = App()
    app.config_dir = config_dir
    # CalledProcessError because the script failed
    with pytest.raises(subprocess.CalledProcessError):
        ConfigHandler(app)


def test_success_confighandler(config_editor, tmp_dir):
    config_editor, config_dir = config_editor
    os.mkdir(os.path.join(tmp_dir, "series_dirs"))
    os.mkdir(os.path.join(tmp_dir, "input_dir"))
    config_editor({
        "series_dirs": [os.path.join(tmp_dir, "series_dirs")],
        "input_dir": os.path.join(tmp_dir, "input_dir")
    })
    app = App()
    app.config_dir = config_dir
    ConfigHandler(app)
