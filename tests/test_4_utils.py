import pytest
import random

from tests.utils.vars import VFILE_NAME_LIST

from video_file_organizer.utils import get_guessit, get_vfile_guessit, \
    Matcher, Transferer
from video_file_organizer.models import VideoFile, OutputFolder


def test_get_guessit():
    assert get_guessit('') is None

    for name in VFILE_NAME_LIST:
        get_guessit(name)


def test_get_vfile_guessit():
    with pytest.raises(TypeError):
        get_vfile_guessit('')

    vfile = VideoFile()
    with pytest.raises(AttributeError):
        get_vfile_guessit(vfile)

    class Fake:
        pass

    fake_vfile = Fake()
    setattr(fake_vfile, 'name',
            VFILE_NAME_LIST[random.randint(0, len(VFILE_NAME_LIST) - 1)])
    with pytest.raises(TypeError):
        get_vfile_guessit(fake_vfile)

    vfile.name = VFILE_NAME_LIST[random.randint(0, len(VFILE_NAME_LIST) - 1)]
    get_vfile_guessit(vfile)


def test_matcher_init(tmp_dir):
    with pytest.raises(TypeError):
        Matcher('')

    class Fake:
        pass

    output_folder = Fake()
    with pytest.raises(TypeError):
        Matcher(output_folder)

    output_folder = OutputFolder(tmp_dir)
    Matcher(output_folder)


def test_transferer_init():
    Transferer()
