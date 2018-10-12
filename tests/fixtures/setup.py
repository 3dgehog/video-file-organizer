import pytest
import zipfile
import tempfile
import shutil
import os

from video_file_organizer.configs.config import CONFIG_TEMPLATES

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "../assets")
CONFIG_DIR = 'config/video_file_organizer/'
ASSET_RULES = {
    "Series": {
        "Boruto": {},
        "Gintama": {},
        "Mahoutsukai no Yome": {},
        "One Piece": {},
        "American Dad": {},
        "Arrow": {},
        "Brooklyn Nine Nine": {},
        "Fresh off the Boat": {},
        "Homeland": {},
        "Lucifer": {},
        "Marvels Agents of S.H.I.E.L.D": {},
        "Supernatural": {},
        "The Big Bang Theory": {},
        "The Flash": {},
        "Vikings": {},
        "That 70s Show": {}
    }
}


@pytest.fixture
def tmp_dir():
    """Creates a temp folder which is deleted after used"""
    tmpdir = tempfile.mkdtemp()
    yield tmpdir
    shutil.rmtree(tmpdir)


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
def tmp_input_dir():
    """Returns a temp folder with sample input dir files which
    is deleted after being used"""
    tmpdir = tempfile.mkdtemp()
    input_zip = os.path.join(ASSETS_DIR, 'input_dir.zip')
    with zipfile.ZipFile(input_zip, "r") as zip_ref:
        zip_ref.extractall(tmpdir)
    yield tmpdir
    shutil.rmtree(tmpdir)


@pytest.fixture
def tmp_series_dirs():
    """Returns a list with 2 dirs populated with series and animes,
    they are deleted after used"""
    # Extract Series
    series_dir_series = tempfile.mkdtemp()
    series_zip = os.path.join(ASSETS_DIR, 'series_dir_series.zip')
    with zipfile.ZipFile(series_zip, "r") as zip_ref:
        zip_ref.extractall(series_dir_series)
    # Extract Animes
    series_dir_anime = tempfile.mkdtemp()
    anime_zip = os.path.join(ASSETS_DIR, 'series_dir_anime.zip')
    with zipfile.ZipFile(anime_zip, "r") as zip_ref:
        zip_ref.extractall(series_dir_anime)

    yield [series_dir_series, series_dir_anime]
    shutil.rmtree(series_dir_series)
    shutil.rmtree(series_dir_anime)
