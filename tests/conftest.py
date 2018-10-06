import pytest
import tempfile
import shutil

# NOTE: A file for all the fixtures that needs to be shared


@pytest.fixture
def tmp_dir():
    """Creates a temp folder which is deleted after used"""
    tmpdir = tempfile.mkdtemp()
    yield tmpdir
    shutil.rmtree(tmpdir)
