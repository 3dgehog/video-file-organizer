from video_file_organizer.handlers.event import EventHandler
from video_file_organizer.models import FileSystemEntry

VALID_EVENT = EventHandler().event_listeners_list.keys()


def set_on_event(event: str, order=10):
    """Adds attr events on function with a tuple of the event and order"""
    if event not in VALID_EVENT:
        raise ValueError("Event {} is not a valid event".format(event))

    def _set_on_event(func):
        if hasattr(func, 'events'):
            func.events.append((event, order))
        else:
            func.events = [(event, order)]

        return func
    return _set_on_event


def get_fse_from_args(args) -> FileSystemEntry:
    for arg in args:
        if isinstance(arg, FileSystemEntry):
            return arg
    raise ValueError("FileSystemEntry argument wasn't passed")
