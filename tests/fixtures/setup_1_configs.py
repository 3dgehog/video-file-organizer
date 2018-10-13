import pytest
import os
import yaml
import shutil
import tempfile


from video_file_organizer.configs.config import CONFIG_TEMPLATES

CONFIG_DIR = 'config/video_file_organizer/'


def copy_config_template_to_dir(path):
    """Copies config_template files to path"""
    for file in os.listdir(CONFIG_TEMPLATES):
        shutil.copyfile(
            os.path.join(CONFIG_TEMPLATES, file),
            os.path.join(path, file))


@pytest.fixture
def config_editor():
    CONFIG_DIR = tempfile.mkdtemp()

    copy_config_template_to_dir(CONFIG_DIR)

    def config_editor(data):
        if data is not None:
            with open(os.path.join(CONFIG_DIR, "config.yaml"), 'r') as yml:
                configyaml = yaml.load(yml)
            for key, value in data.items():
                configyaml[key] = value
            with open(os.path.join(CONFIG_DIR, 'config.yaml'), 'w') as yml:
                yaml.dump(configyaml, yml, default_flow_style=False)

    yield (config_editor, CONFIG_DIR)

    shutil.rmtree(CONFIG_DIR)
