import os
import sys
import subprocess
import logging
import yaml

from typing import Optional, List, Union
from jinja2 import Template

from .base import ConfigBase
from .vars import CONFIG_FILE_TEMPLATE

from video_file_organizer.entries import VideoFileEntry
from video_file_organizer.utils import Observer

logger = logging.getLogger('vfo.config.config')


class Config(Observer, ConfigBase):
    default_filename = 'config.yaml'
    default_path = os.path.join(
        os.environ['HOME'],
        f'.config/video_file_organizer/{default_filename}'
    )

    def __init__(self, args):
        self.args = args

        self.custom_path = self.validate_custom_config_file(
            self.search_config('config_file')
        )

        self.input_dir = self.validate_input_dir(
            self.search_config('input_dir', required=True)
        )

        self.series_dirs = self.validate_series_dirs(
            self.search_config('series_dirs', required=True)
        )

        self.ignore = self.search_config('ignore')

        self.on_transfer_scripts = self.search_config(
            'on_transfer',
            arg_name='on_transfer_scripts'
        )

        self.schedule = self.validate_schedule(
            self.search_config('schedule')
        )

        self.run_before_scripts(self.search_config('before_scripts'))

        self.videoextensions = ['mkv', 'm4v', 'avi', 'mp4', 'mov']

    def validate_custom_config_file(
            self, path: Optional[List[str]]
    ) -> Optional[str]:
        if not path:
            return

        if len(path) > 1:
            raise ValueError('More than 1 config file has been provided')

        if not os.path.exists(path[0]):
            raise FileNotFoundError(f"File {path[0]} doesn't exists")

        fileextension = path[0].rpartition('.')[-1]
        if fileextension not in ['yaml', 'yml']:
            raise TypeError('File needs to be a .yaml format')

        logger.debug(f"Got config file {path[0]}")
        return path[0]

    def validate_input_dir(self, path: Union[str, list]) -> str:
        if not isinstance(path, list):
            path = [path]

        if len(path) > 1:
            raise ValueError('More than 1 input dir has been provided')

        if not os.path.exists(path[0]):
            raise FileNotFoundError(f"File {path[0]} doesn't exists")

        logger.debug(f"Got input dir {path[0]}")
        return path[0]

    def validate_series_dirs(self, dirs: List[str]) -> list:
        for path in dirs:
            if not os.path.exists(path):
                raise FileNotFoundError(
                    f"Series Directory '{path}' doesn't exists")

        logger.debug(f"Got series dirs '{dirs}'")
        return dirs

    def validate_schedule(self, minutes: int):
        if not minutes:
            return
        if isinstance(minutes, list):
            minutes = minutes[0]
        if isinstance(minutes, str):
            minutes = int(minutes)
        if not isinstance(minutes, int):
            raise ValueError('Schduler needs to be an integer')

        return minutes

    @staticmethod
    def create_file_from_template():
        """Creates config.yaml from template"""
        if os.path.exists('config.yaml'):
            logger.info("config.yaml already exists")
            return

        config_file = open('config.yaml', "w")
        config_file.write(CONFIG_FILE_TEMPLATE)
        config_file.close()

    def load_file(self, path: str, **kwargs) -> dict:
        if not os.path.exists(path):
            raise FileNotFoundError("Config file doesn't exist")

        with open(path, 'r') as yml:
            return yaml.load(yml, Loader=yaml.FullLoader)

    def run_before_scripts(self, scripts: Union[List[str], None]):
        if not scripts:
            logger.debug("No before scripts to run")
            return

        for script in scripts:
            logger.debug(f"Running before script '{script}'")
            self._run_script(script)
            logger.debug(f"Ran script {script}")

    def update(self, *args, topic: str, **kwargs):
        if topic == 'Transferer/after':
            self.run_on_transfer_scripts(kwargs['vfile'])

    def run_on_transfer_scripts(self, vfile: VideoFileEntry):
        if not self.on_transfer_scripts:
            return
        for script in self.on_transfer_scripts:
            logger.debug(f"Running on_transfer for vfile: '{vfile.name}'")
            values: dict = {}
            values.update(vars(vfile))
            values.update(vars(vfile)['metadata'])
            rendered_script = Template(script).render(values)
            self._run_script(rendered_script)

    def _run_script(self, script: str):
        try:
            subprocess.run([script], shell=True, check=True)
        except subprocess.CalledProcessError as e:
            logger.info(e)
            sys.exit()
