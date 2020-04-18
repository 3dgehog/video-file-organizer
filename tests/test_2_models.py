import pytest

from video_file_organizer.models import FolderCollection, VideoCollection, \
    VideoFile


def test_folder_collection(tmp_dir, sample_series_dirs):

    # Test path that doesn't exist
    with pytest.raises(FileNotFoundError):
        FolderCollection('random/path')

    # Test that there isn't any entries in empty folder
    assert len(FolderCollection(tmp_dir)._entries) == 0

    # Test that there is entires from sample series dir
    assert len(FolderCollection(sample_series_dirs)) > 0


def test_video_collection(tmp_dir, sample_input_dir):

    # Test path that doesn't exist
    with pytest.raises(FileNotFoundError):
        VideoCollection('./random/path')

    # Test that there isn't entries in empty folder
    assert len(VideoCollection(sample_input_dir, videoextensions=[
        'mkv', 'm4v', 'avi', 'mp4', 'mov']).entries) > 0

    # Test that entry as added successfully
    vc = VideoCollection(tmp_dir, videoextensions=[
        'mkv', 'm4v', 'avi', 'mp4', 'mov'])
    vc.add_vfile('hello')
    assert len([x for x in vc if x.name == 'hello']) > 0

    # Test retrieving vfile that doesn't exist
    with pytest.raises(ValueError):
        vc.get_vfile('random')

    # Test retrieving vfile that does exist
    for vfile in vc:
        if vfile.name == 'hello':
            hello_vfile = vfile
    assert vc.get_vfile('hello') == hello_vfile


def test_video_file():

    # Test VideoFile initiates without values
    assert VideoFile()

    # Test VideoFile init with kwargs
    vfile = VideoFile(**{'name': 'test', 'path': 'here'})
    assert vfile.name == 'test' and vfile.path == 'here'

    vfile = VideoFile()

    # Test editing attribute that doesn't exist
    with pytest.raises(ValueError):
        vfile.edit('hi')

    # Test editing attribute that doesn't exist
    with pytest.raises(AttributeError):
        vfile.edit(**{'random': 'random'})

    # Test editing a valid attribute
    vfile.edit(path='./random/path')
    assert vfile.path == './random/path'
