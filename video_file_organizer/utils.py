from typing import Set

from video_file_organizer.models import VideoFile


def vfile_options(*options):
    for arg in options:
        if not hasattr(VideoFile(), arg):
            raise KeyError(f"VideoFile doesn't have attribute {arg}")

    def decorator(fn):
        def wrapper(*args, vfile: VideoFile, **kwargs):

            if not isinstance(vfile, VideoFile):
                raise TypeError("vfile needs to be an instance of VideoFile")

            data = vfile.get_attr(*options)
            results = fn(*args, vfile=vfile, **data, **kwargs)
            if results:
                vfile.edit(**results)
                return True

            return False
        return wrapper
    return decorator


class Observer:
    def update(self, *arg, topic: str, **kwargs):
        pass


class Observee:
    _observers: Set[Observer] = set()

    def attach(self, observer):
        self._observers.add(observer)

    def detach(self, observer):
        self._observers.discard(observer)

    def notify(self, *args, topic: str, **kwargs):
        for observer in self._observers:
            observer.update(*args, topic=topic, **kwargs)
