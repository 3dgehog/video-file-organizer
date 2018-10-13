import pytest
import tempfile
import shutil
import os
import zipfile


ASSETS_DIR = os.path.join(os.path.dirname(__file__), "../assets")


class App:
    def _requirements(self, requirements: list):
        for require in requirements:
            if require not in dir(self):
                raise AttributeError(
                    "Missing attributes {} in app".format(require))


@pytest.fixture
def tmp_dir():
    """Creates a temp folder which is deleted after used"""
    tmpdir = tempfile.mkdtemp()
    yield tmpdir
    shutil.rmtree(tmpdir)


@pytest.fixture
def extract_input_dir():
    """Returns a temp folder with sample input dir files which
    is deleted after being used"""
    tmpdir = tempfile.mkdtemp()
    input_zip = os.path.join(ASSETS_DIR, 'input_dir.zip')
    with zipfile.ZipFile(input_zip, "r") as zip_ref:
        zip_ref.extractall(tmpdir)
    yield tmpdir
    shutil.rmtree(tmpdir)


@pytest.fixture
def extract_series_dirs():
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
