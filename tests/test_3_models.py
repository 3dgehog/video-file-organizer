import pytest

from video_file_organizer.models import Folder


def test_folder_init(tmp_file, tmp_dir):
    with pytest.raises(TypeError):
        Folder()

    with pytest.raises(FileNotFoundError):
        Folder('/path/that/doesnt/exist')

    with pytest.raises(NotADirectoryError):
        Folder(tmp_file)

    with pytest.raises(FileNotFoundError):
        Folder([tmp_dir, '/path/that/doesnt/exist'])

    Folder([tmp_dir, tmp_dir])


def test_output_folder_init():
    pass


def test_input_folder_init():
    pass
