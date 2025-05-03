from functools import wraps


def field_validation(handler, cls, value):
    @wraps(handler)
    def wrapper():
        result = handler(cls, value)
        return result

    return wrapper
