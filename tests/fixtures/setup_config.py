import pytest
import tempfile
import os
import shutil
import yaml

from video_file_organizer.configs.config_handler \
    import ConfigHandler
from video_file_organizer.configs.config import CONFIG_TEMPLATES


CONFIG_DIR = 'config/video_file_organizer/'


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


@pytest.fixture()
def tmp_config_populated(tmp_config_editor, tmp_input_dir, tmp_series_dirs):
    """Returns ConfigHandler object with input_dir and series_dirs populated by
    the assets folder"""
    _editor, tmp_config_dir = tmp_config_editor
    _editor({
        "input_dir": tmp_input_dir,
        "series_dirs": tmp_series_dirs
    })
    return ConfigHandler(tmp_config_dir)
