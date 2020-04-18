import os
import yaml
import configparser
import shutil

from video_file_organizer.app import App
from video_file_organizer.config import CONFIG_FILE_TEMPLATE_LOCATION, \
    RULEBOOK_FILE_TEMPLATE_LOCATION


def setup_app_with_injectors(config_dir):
    """Returns app, config_injector and rule_book_injector"""
    app = App()
    app.config_dir = config_dir
    config_injector = ConfigFileInjector(config_dir)
    rule_book_injector = RuleBookFileInjector(config_dir)
    return app, config_injector, rule_book_injector


def empty_folder(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


class ConfigFileInjector:
    """A class that helps inject the configs in the config.yaml"""

    def __init__(self, config_dir):
        self.config_dir = config_dir
        self.path = os.path.join(self.config_dir, 'config.yaml')
        self.copy_config_file_template()
        self.configvalue = self._get_configvalue()

    def update(self, data):
        if data is not None:
            for key, value in data.items():
                self.configvalue[key] = value
            self._save()

    def _save(self):
        with open(self.path, 'w') as yml:
            yaml.dump(self.configvalue, yml, default_flow_style=False)

    def _get_configvalue(self):
        with open(self.path, 'r') as yml:
            configyaml = yaml.load(yml, Loader=yaml.FullLoader)
        return configyaml

    def copy_config_file_template(self):
        shutil.copyfile(
            CONFIG_FILE_TEMPLATE_LOCATION,
            os.path.join(self.config_dir, 'config.yaml'))


class RuleBookFileInjector:
    """A class that helps inject the rules in the rule_book.ini"""

    def __init__(self, config_dir):
        self.config_dir = config_dir
        self.path = os.path.join(self.config_dir, 'rule_book.ini')
        self.copy_config_file_template()
        self.configparse = self._get_configpaser()

    def _get_configpaser(self):
        configparse = configparser.ConfigParser(allow_no_value=True)
        configparse.read(self.path)
        return configparse

    def update(self, section, data):
        if section is not None:
            self.configparse[section] = data
            self._save()

    def _save(self):
        with open(self.path, 'w') as configfile:
            self.configparse.write(configfile)

    def copy_config_file_template(self):
        shutil.copyfile(
            RULEBOOK_FILE_TEMPLATE_LOCATION,
            os.path.join(self.config_dir, 'rule_book.ini'))
