from video_file_organizer.events import VALID_EVENT


# def set_before_match(func):
#     if hasattr(func, 'event'):
#         func.event.append('before_match')
#     else:
#         func.event = ['before_match']
#     return func


# def set_after_match(func):
#     if hasattr(func, 'event'):
#         func.event.append('after_match')
#     else:
#         func.event = ['after_match']
#     return func


# def set_before_transfer(func):
#     if hasattr(func, 'event'):
#         func.event.append('before_transfer')
#     else:
#         func.event = ['before_transfer']
#     return func


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
