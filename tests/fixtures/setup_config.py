import pytest
import os
import yaml


@pytest.fixture
def tmp_config_editors(tmp_config_dir):
    """Returns an editor that takes a dict to change the values in config.yaml and
    updates them and the path to the config_dir"""
    def config_editor(data):
        if data is not None:
            with open(os.path.join(tmp_config_dir, "config.yaml"), 'r') as yml:
                configyaml = yaml.load(yml)
            for key, value in data.items():
                configyaml[key] = value
            with open(os.path.join(tmp_config_dir, 'config.yaml'), 'w') as yml:
                yaml.dump(configyaml, yml, default_flow_style=False)

    def rule_editor(data):
        if data is not None:
            with open(os.path.join(
                    tmp_config_dir, "rule_book.yaml"), 'r') as yml:
                ruleyaml = yaml.load(yml)
            for key, value in data.items():
                ruleyaml[key] = value
            with open(os.path.join(
                    tmp_config_dir, 'rule_book.yaml'), 'w') as yml:
                yaml.dump(ruleyaml, yml, default_flow_style=False)

    return config_editor, rule_editor, tmp_config_dir


@pytest.fixture()
def tmp_config_editor_populated(
        tmp_config_editors, tmp_input_dir, tmp_series_dirs):
    """Returns ConfigHandler object with input_dir and series_dirs populated by
    the assets folder"""
    config_editor, rule_editor, tmp_config_dir = tmp_config_editors
    config_editor({
        "input_dir": tmp_input_dir,
        "series_dirs": tmp_series_dirs
    })
    return config_editor, rule_editor, tmp_config_dir
