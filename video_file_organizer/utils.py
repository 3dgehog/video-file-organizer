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

    @classmethod
    def notify(cls, *args, topic: str, **kwargs):
        for observer in cls._observers:
            observer.update(*args, topic=topic, **kwargs)


def vfile_consumer(fn):
    def wrapper(self, vfile: VideoFile, **kwargs):

        if not isinstance(vfile, VideoFile):
            raise TypeError(
                "vfile needs to be an instance of VideoFile")

        data = vfile.get_attr()

        logger.debug(f'***>>> {self.__class__.__name__} <<<***')

        Observee.notify(
            topic=f'{self.__class__.__name__}/before',
            vfile=vfile
        )

        results = fn(self, vfile=vfile, **data, **kwargs)

        if not isinstance(results, dict):
            raise ValueError("Expected a dictionary")

        vfile.update(**results)
        if results.get('error_msg'):
            vfile.update(valid=False)
            logger.info(f"ERROR_MSG: {results['error_msg']}")
            return

        Observee.notify(
            topic=f'{self.__class__.__name__}/after',
            vfile=vfile
        )

        return
    return wrapper
