import pytest
import tempfile
import os
import shutil
import yaml
import subprocess
from video_file_organizer.config_handler import ConfigHandler, CONFIG_TEMPLATES


CONFIG_DIR = 'config/video_file_organizer/'


def test_empty_config_folder(tmp_dir):
    """Test ValueError Exception on new empty config folder which indirectly
    tests:
    - Creation of new configs from templates
    - Opening and reading config.yaml
    - If all required fields are entered"""
    config_dir = os.path.join(tmp_dir, CONFIG_DIR)
    # ValueError because the required fields are not entered
    with pytest.raises(ValueError):
        ConfigHandler(config_dir=config_dir)
    # Checks the files where created by the ConfigHandler
    assert os.path.exists(config_dir)


@pytest.fixture
def tmp_config_dir():
    """Makes a copy of config_templates to a temp folder and returns the config
    folder location"""
    tmpdir = tempfile.mkdtemp()
    tmp_config_dir = os.path.join(tmpdir, CONFIG_DIR)
    os.makedirs(tmp_config_dir)
    for file in os.listdir(CONFIG_TEMPLATES):
        shutil.copyfile(
            os.path.join(CONFIG_TEMPLATES, file),
            os.path.join(tmp_config_dir, file))
    yield tmp_config_dir
    shutil.rmtree(tmpdir)


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


def test_none_existing_series_and_input_dirs(tmp_config_editor, tmp_dir):
    """Test ValueError on missing series_dirs in config.yaml"""
    editor, config_dir = tmp_config_editor
    editor({
        "series_dirs": [os.path.join(config_dir, "series_dirs")],
        "input_dir": os.path.join(tmp_dir, "input_dir")
    })
    # FileNoteFoundError because the directory doesn't exist
    with pytest.raises(FileNotFoundError):
        ConfigHandler(config_dir=config_dir)


def add_empty_series_and_input_dirs(editor, tmp_dir):
    """Adds series_dirs and input_dir config to config file and
    makes empty directories to tmp_dir"""
    os.mkdir(os.path.join(tmp_dir, "series_dirs"))
    os.mkdir(os.path.join(tmp_dir, "input_dir"))
    editor({
        "series_dirs": [os.path.join(tmp_dir, "series_dirs")],
        "input_dir": os.path.join(tmp_dir, "input_dir")
    })


def test_failing_before_script(tmp_config_editor, tmp_dir):
    """Test if there is a fail before script"""
    editor, config_dir = tmp_config_editor
    add_empty_series_and_input_dirs(editor, tmp_dir)
    editor({
        "before_scripts": [os.path.join(
            os.path.dirname(__file__), "assets/fail_script.sh")]
    })
    # CalledProcessError because the script failed
    with pytest.raises(subprocess.CalledProcessError):
        ConfigHandler(config_dir=config_dir)
