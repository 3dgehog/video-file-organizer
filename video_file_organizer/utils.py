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


class VFileAddons:
    def vfile_consumer(fn):
        def wrapper(self, vfile: VideoFile, **kwargs):

            if not isinstance(vfile, VideoFile):
                raise TypeError(
                    "vfile needs to be an instance of VideoFile")

            data = vfile.get_attr()

            logger.debug(f'>>> {self.__class__.__name__} <<<')

            Observee.notify(
                topic=f'{self.__class__.__name__}/before',
                vfile=vfile
            )

            results = fn(self, vfile=vfile, **data, **kwargs)

            if results and type(results) == bool:
                pass
            elif results:
                vfile.update(**results)
            else:
                vfile.update(valid=False)

            Observee.notify(
                topic=f'{self.__class__.__name__}/after',
                vfile=vfile
            )

            return
        return wrapper
