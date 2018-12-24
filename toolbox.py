import os
import zipfile
import logging
import argparse
import shutil

from tests.utils.injectors import ConfigInjector, RuleBookInjector
from tests.fixtures.setup_assets import SERIES_CONFIGPARSE

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument("--mock",
                    help="Creates a mock folder",
                    action="store_true")
args = parser.parse_args()

MOCK_FOLDER = os.path.join(
    os.path.dirname(__file__), 'mock')

CONFIG_TEMPLATES = os.path.join(os.path.dirname(
    __file__), 'video_file_organizer/config_templates')

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
    config_injector = ConfigInjector(config_folder_path)
    rule_book_injector = RuleBookInjector(config_folder_path)

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
    rule_book_injector.configparse['series'] = SERIES_CONFIGPARSE
    rule_book_injector.save()
    config_injector.append({
        "input_dir": input_folder_path,
        "series_dirs": [series_dir_path, anime_dir_path]
    })


if args.mock:
    setup_mock()
    logging.info(
        "Run `pipenv run vfo -c mock/configs` \
to run against mock folder")
