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
        if not isinstance(observer, Observer):
            raise TypeError(
                'To attach to an Observee, you need the subclass of Observer')
        self._observers.add(observer)

    def attach_multiple(self, observers: list):
        for observer in observers:
            self.attach(observer)

    def detach(self, observer):
        self._observers.discard(observer)

    def detach_all(self):
        self._observers = set()

    def notify(self, *args, topic: str, **kwargs):
        for observer in self._observers:
            observer.update(*args, topic=topic, **kwargs)
