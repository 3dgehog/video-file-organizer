import abc
import logging
from typing import Set

from video_file_organizer.entries import VideoFileEntry

logger = logging.getLogger('vfo.utils')


class Observer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def update(self, *arg, topic: str, **kwargs):
        pass


class Observee:
    _observers: Set[Observer] = set()

    @classmethod
    def attach(cls, observer):
        cls._observers.add(observer)

    @classmethod
    def detach(cls, observer):
        cls._observers.discard(observer)

    @classmethod
    def notify(cls, *args, topic: str, **kwargs):
        for observer in cls._observers:
            observer.update(*args, topic=topic, **kwargs)


def vfile_consumer(name):
    def wrapper(fn):
        def wrapped_function(vfile: VideoFileEntry):

            if not isinstance(vfile, VideoFileEntry):
                raise TypeError(
                    "vfile needs to be an instance of VideoFileEntry")

            Observee.notify(topic=f'{name}/before',
                            vfile=vfile)

            fn(vfile)

            Observee.notify(topic=f'{name}/after',
                            vfile=vfile)

        return wrapped_function
    return wrapper
