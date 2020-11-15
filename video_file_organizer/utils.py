import abc
import logging
from typing import Set


logger = logging.getLogger('vfo.utils')


class Observer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def update(self, *arg, topic: str, **kwargs):
        pass


class Observee:
    _active_observers: Set[Observer] = set()
    _registered_observers: Set[Observer] = set()

    def __init__(self):
        pass

    def attach_observer(self, observer):
        if not isinstance(observer, Observer):
            raise TypeError(
                'To attach to an Observee, you need the subclass of Observer')
        self._active_observers.add(observer)

    def attach_multiple_observers(self, observers: list):
        for observer in observers:
            self.attach_observer(observer)

    def detach_observer(self, observer):
        self._active_observers.discard(observer)

    def detach_all_observers(self):
        self._active_observers = set()

    def register_observer(self, observer):
        if not isinstance(observer, Observer):
            raise TypeError(
                'To attach to an Observee, you need the subclass of Observer')
        self._registered_observers.add(observer)

    def register_multiple_observers(self, observers):
        for observer in observers:
            self.register_observer(observer)

    def __enter__(self):
        self.attach_multiple_observers(self._registered_observers)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.detach_all_observers()

    def notify_observers(self, *args, topic: str, **kwargs):
        logger.debug(f"NOTIFYING Observers about topic: {topic}")
        for observer in self._active_observers:
            observer.update(*args, topic=topic, **kwargs)