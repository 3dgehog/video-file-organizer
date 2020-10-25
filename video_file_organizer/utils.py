import abc
import logging
from typing import Set


logger = logging.getLogger('vfo.utils')


class Observer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def update(self, *arg, topic: str, **kwargs):
        pass


class Observee:
    _observers: Set[Observer] = set()

    def __init__(self):
        pass

    def attach(self, observer):
        self._observers.add(observer)

    def detach(self, observer):
        self._observers.discard(observer)

    def notify(self, *args, topic: str, **kwargs):
        for observer in self._observers:
            observer.update(*args, topic=topic, **kwargs)
