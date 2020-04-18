import pytest
import tempfile
import shutil
import os
import zipfile

from tests.vars import ASSETS_DIR


@pytest.fixture
def tmp_file():
    tmpfile = tempfile.mkstemp()[1]
    yield tmpfile
    os.remove(tmpfile)


@pytest.fixture
def tmp_dir():
    """Creates a temp folder which is deleted after used"""
    tmpdir = tempfile.mkdtemp()
    yield tmpdir
    shutil.rmtree(tmpdir)


@pytest.fixture
def sample_input_dir():
    """Returns a temp folder with sample input dir files which
    is deleted after being used"""
    tmpdir = tempfile.mkdtemp()
    input_zip = os.path.join(ASSETS_DIR, 'input_dir.zip')
    with zipfile.ZipFile(input_zip, "r") as zip_ref:
        zip_ref.extractall(tmpdir)
    yield tmpdir
    shutil.rmtree(tmpdir)


@pytest.fixture
def sample_series_dirs():
    """Returns a list with 2 dirs populated with series and animes,
    they are deleted after used"""
    tmp_dir = tempfile.mkdtemp()
    # Extract Series
    os.mkdir(os.path.join(tmp_dir, "series_dir"))
    series_dir_series = os.path.join(tmp_dir, "series_dir")
    series_zip = os.path.join(ASSETS_DIR, 'series_dir_series.zip')
    with zipfile.ZipFile(series_zip, "r") as zip_ref:
        zip_ref.extractall(series_dir_series)
    # Extract Animes
    os.mkdir(os.path.join(tmp_dir, "anime_dir"))
    series_dir_anime = os.path.join(tmp_dir, "anime_dir")
    anime_zip = os.path.join(ASSETS_DIR, 'series_dir_anime.zip')
    with zipfile.ZipFile(anime_zip, "r") as zip_ref:
        zip_ref.extractall(series_dir_anime)

    yield [series_dir_series, series_dir_anime]
    shutil.rmtree(tmp_dir)
