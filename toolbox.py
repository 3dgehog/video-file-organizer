import os
import zipfile
import logging
import argparse
import shutil
import configparser
import subprocess

from tests.utils import ConfigFileInjector, RuleBookFileInjector
from tests.vars import SERIES_CONFIGPARSE

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument("--mock",
                    help="Creates a mock folder",
                    action="store_true")
parser.add_argument("--systemd",
                    help="Creates systemd files",
                    action="store_true")
args = parser.parse_args()

MOCK_FOLDER = os.path.join(
    os.path.dirname(__file__), 'mock')

SYSTEMD_FOLDER = os.path.join(
    os.path.dirname(__file__), 'systemd')


ASSETS_DIR = os.path.join(
    os.path.dirname(__file__), 'tests/assets')


def setup_mock():
    """Creates a mock folder with all the settings and blank folders need to
    test the production software"""
    # Create mock folder
    if os.path.exists(MOCK_FOLDER):
        logging.debug("deleting existing mock folder")
        shutil.rmtree(MOCK_FOLDER)
    logging.debug("creating mock folder")
    os.makedirs(MOCK_FOLDER)

    # Creake config folder in mock folder
    config_folder_path = os.path.join(MOCK_FOLDER, 'configs')
    logging.debug("creating configs folder")
    os.makedirs(config_folder_path)

    logging.debug("initializing config/rule injectors")
    config_injector = ConfigFileInjector(config_folder_path)
    rule_book_injector = RuleBookFileInjector(config_folder_path)

    # Create and extract input folder
    input_folder_path = os.path.join(MOCK_FOLDER, 'input_dir')
    logging.debug("creating input folder")
    os.makedirs(input_folder_path)
    input_zip = os.path.join(ASSETS_DIR, 'input_dir.zip')
    logging.debug("extracting to input folder")
    with zipfile.ZipFile(input_zip, "r") as zip_ref:
        zip_ref.extractall(input_folder_path)

    # Create and extract anime and series folder
    series_dir_path = os.path.join(MOCK_FOLDER, 'series_dir')
    logging.debug("creating series folder")
    os.makedirs(series_dir_path)
    series_zip = os.path.join(ASSETS_DIR, 'series_dir_series.zip')
    logging.debug("extracting to series folder")
    with zipfile.ZipFile(series_zip, "r") as zip_ref:
        zip_ref.extractall(series_dir_path)

    anime_dir_path = os.path.join(MOCK_FOLDER, 'anime_dir')
    logging.debug("creating anime folder")
    os.makedirs(anime_dir_path)
    anime_zip = os.path.join(ASSETS_DIR, 'series_dir_anime.zip')
    logging.debug("extracting to anime folder")
    with zipfile.ZipFile(anime_zip, "r") as zip_ref:
        zip_ref.extractall(anime_dir_path)

    # Inject rules and configs
    logging.debug("injecting default rules and configs")
    rule_book_injector.update('series', SERIES_CONFIGPARSE)
    config_injector.update({
        "input_dir": input_folder_path,
        "series_dirs": [series_dir_path, anime_dir_path]
    })


def setup_systemd():
    systemd_user = input("Which user?: ")
    if not systemd_user:
        logging.warning("software will not work without a user")
        return

    if os.path.exists(SYSTEMD_FOLDER):
        logging.warning("systemd folder already exists, aborting")
        return

    logging.debug("creating systemd folder")
    os.makedirs(SYSTEMD_FOLDER)

    working_dir_path = os.path.dirname(os.path.realpath(__file__))

    pipenv_path = subprocess.check_output(
        "which pipenv", shell=True).decode().replace('\n', '')

    service_file_path = os.path.join(SYSTEMD_FOLDER, 'vfo.service')
    service_config = configparser.ConfigParser()
    service_config.optionxform = str
    service_config['Unit'] = {
        'Description': 'Service file for Video File Organizer',
        'After': 'network.target'
    }
    service_config['Service'] = {
        'User': 'maxence',
        'WorkingDirectory': working_dir_path,
        'ExecStart': f'{pipenv_path} run vfo'
    }
    service_config['Install'] = {
        'WantedBy': 'multi-user.target'
    }
    with open(service_file_path, 'w') as service_file:
        service_config.write(service_file)
        logging.debug("vfo.service created")

    timer_file_path = os.path.join(SYSTEMD_FOLDER, 'vfo.timer')
    timer_config = configparser.ConfigParser()
    timer_config.optionxform = str
    timer_config['Unit'] = {
        'Description': '15 minute timer for video file organizer'
    }
    timer_config['Timer'] = {
        'Unit': 'vfo.service',
        'OnCalendar': '*:0/15'
    }
    timer_config['Install'] = {
        'WantedBy': 'timers.target'
    }
    with open(timer_file_path, 'w') as timer_file:
        timer_config.write(timer_file)
        logging.debug("vfo.service created")
    logging.info("Files are ready in 'systemd/'")


if args.mock:
    setup_mock()


if args.systemd:
    setup_systemd()
