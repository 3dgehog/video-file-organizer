import shutil
import os
import yaml
import configparser

from video_file_organizer.settings import CONFIG_TEMPLATES

from video_file_organizer.app import App


def setup_app_with_injectors(config_dir):
    """Returns app, config_injector and rule_book_injector"""
    app = App()
    app.config_dir = config_dir
    config_injector = ConfigInjector(config_dir)
    rule_book_injector = RuleBookInjector(config_dir)
    return app, config_injector, rule_book_injector


class ConfigInjector:
    """A class that helps inject the configs in the config.yaml"""

    def __init__(self, config_dir):
        self.config_dir = config_dir
        self.config_path = os.path.join(self.config_dir, 'config.yaml')
        self._copy_config_template()
        self.configvalue = self._get_configvalue()

    def append(self, data):
        if data is not None:
            for key, value in data.items():
                self.configvalue[key] = value
            self._save()

    def _save(self):
        with open(self.config_path, 'w') as yml:
            yaml.dump(self.configvalue, yml, default_flow_style=False)

    def _copy_config_template(self):
        for file in os.listdir(CONFIG_TEMPLATES):
            shutil.copyfile(
                os.path.join(CONFIG_TEMPLATES, file),
                os.path.join(self.config_dir, file))
        self._get_configvalue()

    def _get_configvalue(self):
        with open(self.config_path, 'r') as yml:
            configyaml = yaml.load(yml)
        return configyaml


class RuleBookInjector:
    """A class that helps inject the rules in the rule_book.ini"""

    def __init__(self, config_dir):
        self.config_dir = config_dir
        self.rule_book_path = os.path.join(self.config_dir, 'rule_book.ini')
        self.configparse = self._get_configpaser()

    def _get_configpaser(self):
        configparse = configparser.ConfigParser(allow_no_value=True)
        configparse.read(self.rule_book_path)
        return configparse

    def save(self):
        with open(self.rule_book_path, 'w') as configfile:
            self.configparse.write(configfile)
