import pytest

from video_file_organizer.models import VideoFile
from video_file_organizer.utils import VFileAddons, Observer, Observee


def test_vfile_options():
    # Wrong option
    with pytest.raises(KeyError):
        VFileAddons.vfile_options('hi')

    def f1(*args, vfile: VideoFile, **kwargs):
        # Correctly passing kwargs
        assert kwargs['name'] == 'name1'

    # Missing vfile
    with pytest.raises(TypeError):
        VFileAddons.vfile_options('name')(f1)('hi')

    vfile = VideoFile()
    vfile.edit(name='name1')
    VFileAddons.vfile_options('name')(f1)(vfile=vfile)

    def f2(*args, vfile: VideoFile, **kwargs):
        return {'name': 'name2'}

    VFileAddons.vfile_options('name')(f2)(vfile=vfile)
    # Successfully update attribute
    assert vfile.name == 'name2'

    def f3(*args, vfile: VideoFile, **kwargs):
        return False

    # Successfully returned bool
    assert VFileAddons.vfile_options('name')(f2)(vfile=vfile) is True
    assert VFileAddons.vfile_options('name')(f3)(vfile=vfile) is False


def test_oberserver():
    assert hasattr(Observer, 'update')


def test_oberservee():
    observer = Observer()
    observee = Observee()

    # Able to attech successfully
    observee.attach(observer)
    assert observer in observee._observers

    # Update observer successfully
    def new_update(*arg, topic: str, **kwargs):
        assert topic == 'new_topic'
    observer.update = new_update
    observee.notify(topic='new_topic')

    # Able to detach successfully
    observee.detach(observer)
    assert observer not in observee._observers
