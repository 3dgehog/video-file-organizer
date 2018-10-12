def set_before_match(func):
    if hasattr(func, 'event'):
        func.event.append('before_match')
    else:
        func.event = ['before_match']
    return func


def set_after_match(func):
    if hasattr(func, 'event'):
        func.event.append('after_match')
    else:
        func.event = ['after_match']
    return func


def set_before_transfer(func):
    if hasattr(func, 'event'):
        func.event.append('before_transfer')
    else:
        func.event = ['before_transfer']
    return func
