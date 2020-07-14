import abc
import logging
from typing import Set

from video_file_organizer.models import VideoFile

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

    def notify(self, *args, topic: str, **kwargs):
        logger.debug(f"********* {topic} *********")
        for observer in self._observers:
            observer.update(*args, topic=topic, **kwargs)


class VFileConsumer(Observee):
    def vfile_consumer(*options):
        def decorator(fn):
            def wrapper(*args, vfile: VideoFile, **kwargs):
                obj = args[0]

                if not isinstance(vfile, VideoFile):
                    raise TypeError(
                        "vfile needs to be an instance of VideoFile")

                data = vfile.get_attr(*options)

                obj.notify(
                    topic=f'{obj.__class__.__name__}/before',
                    vfile=vfile
                )

                results = fn(*args, vfile=vfile, **data, **kwargs)

                if not results:
                    return False

                vfile.update(**results)

                obj.notify(
                    topic=f'{obj.__class__.__name__}/after',
                    vfile=vfile
                )

                return True
            return wrapper
        return decorator
