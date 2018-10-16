import logging


VALID_EVENT = [
    'before_match', 'after_match', 'before_transfer', 'after_transfer'
]

logger = logging.getLogger('app.events')
logger.setLevel(logging.INFO)


class EventHandler:
    def __init__(self, app):
        logger.debug("Initializing EventHandler")
        self.app = app
        self.event_before_match = Event()
        self.event_after_match = Event()
        self.event_before_transfer = Event()
        self.event_after_transfer = Event()
        self.event_listeners_list = {
            "before_match": self.event_before_match.add_listener,
            "after_match": self.event_after_match.add_listener,
            "before_transfer": self.event_before_transfer.add_listener,
            "after_transfer": self.event_after_transfer.add_listener
        }

    def before_match(self, *args, **kwargs):
        logger.debug("running before match event")
        self.event_before_match.notify(*args, **kwargs)

    def after_match(self, *args, **kwargs):
        logger.debug("running after match event")
        self.event_after_match.notify(*args, **kwargs)

    def before_transfer(self, *args, **kwargs):
        logger.debug("running before transfer event")
        self.event_before_transfer.notify(*args, **kwargs)

    def after_transfer(self, *args, **kwargs):
        logger.debug("running after transfer event")
        self.event_after_transfer.notify(*args, **kwargs)


class Event:
    def __init__(self):
        self._listeners: list = []

    def add_listener(self, listener):
        self._listeners.append(listener)

    def notify(self, *args, **kwargs):
        for func in self._listeners:
            func(*args, **kwargs)
