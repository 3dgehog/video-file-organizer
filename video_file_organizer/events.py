class EventHandler:
    def __init__(self, app):
        self.app = app
        self.event_before_match = Event()
        self.event_after_match = Event()
        self.event_before_transfer = Event()
        self.event_list = {
            "before_match": self.event_before_match.add_listener,
            "after_match": self.event_after_match.add_listener,
            "before_transfer": self.event_before_transfer.add_listener
        }

    def before_match(self, *args, **kwargs):
        self.event_before_match.notify(args, kwargs)

    def after_match(self, *args, **kwargs):
        self.event_after_match.notify(args, kwargs)

    def before_transfer(self, *args, **kwargs):
        self.event_before_transfer.notify(args, kwargs)


class Event:
    def __init__(self):
        self._listeners: list = []

    def add_listener(self, listener):
        self._listeners.append(listener)

    def notify(self, *args, **kwargs):
        for func in self._listeners:
            func(args, kwargs)