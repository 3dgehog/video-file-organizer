from video_file_organizer.handlers.event import VALID_EVENT


DEFAULT_ORDER = 10


def set_on_event(event: str, order=DEFAULT_ORDER):
    """Adds attr events on function with a tuple of the event and order"""
    if event not in VALID_EVENT:
        raise ValueError("Event {} is not a valid event".format(event))

    def _set_on_event(func):
        if hasattr(func, 'event'):
            func.events.append((event, order))
        else:
            func.events = [(event, order)]

        return func
    return _set_on_event
