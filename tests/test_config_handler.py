import pytest
import os
import shutil
import yaml
import subprocess
from video_file_organizer.config_handler import ConfigHandler, CONFIG_TEMPLATES


CONFIG_DIR = 'config/video_file_organizer/'


def test_new_folder_confighandler(new_temp_dir):
    """Test ValueError Exception on new empty config folder which indirectly
    tests:
    - Creation of new configs from templates
    - Opening and reading config.yaml"""
    config_dir = new_temp_dir
    with pytest.raises(ValueError):
        ConfigHandler(config_dir=config_dir)


@pytest.fixture
def tmp_config_dir(new_temp_dir):
    """Makes a copy of config_templates to a temp folder and returns the config
    folder location"""
    config_dir = os.path.join(new_temp_dir, CONFIG_DIR)
    os.makedirs(config_dir)
    for file in os.listdir(CONFIG_TEMPLATES):
        shutil.copyfile(
            os.path.join(CONFIG_TEMPLATES, file),
            os.path.join(config_dir, file))
    return config_dir


@pytest.fixture
def tmp_config_editor(tmp_config_dir):
    """Returns an editor that takes a dict to change the values in config.yaml and
    updates them and the path to the config_dir"""
    def _editor(data):
        if data is not None:
            with open(os.path.join(tmp_config_dir, "config.yaml"), 'r') as yml:
                configyaml = yaml.load(yml)
            for key, value in data.items():
                configyaml[key] = value
            with open(os.path.join(tmp_config_dir, 'config.yaml'), 'w') as yml:
                yaml.dump(configyaml, yml, default_flow_style=False)
    return _editor, tmp_config_dir


def test_series_dirs_missing(tmp_config_editor):
    """Test ValueError on missing series_dirs in config.yaml"""
    editor, config_dir = tmp_config_editor
    editor({
        "series_dirs": [os.path.join(config_dir, "series_dirs")]
    })
    with pytest.raises(ValueError):
        ConfigHandler(config_dir=config_dir)


def add_series_dirs(editor, config_dir):
    """Added series_dirs to config file and directory"""
    os.mkdir(os.path.join(config_dir, "series_dirs"))
    editor({"series_dirs": [os.path.join(config_dir, "series_dirs")]})


def test_failing_before_script(tmp_config_editor):
    """Test if there is a fail before script"""
    editor, config_dir = tmp_config_editor
    add_series_dirs(editor, config_dir)
    editor({
        "before_scripts": [os.path.join(
            os.path.dirname(__file__), "assets/fail_script.sh")]
    })
    with pytest.raises(subprocess.CalledProcessError):
        ConfigHandler(config_dir=config_dir)
