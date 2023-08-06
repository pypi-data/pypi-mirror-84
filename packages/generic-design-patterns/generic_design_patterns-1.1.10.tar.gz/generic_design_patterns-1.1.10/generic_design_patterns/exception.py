from . import log

# TODO: test


class AbstractExceptionHandler(object):
    def __call__(self, exception, *args, **kwargs):
        pass


class WrapToNewException(AbstractExceptionHandler):
    def __init__(self, wrapper, message_generator):
        self.message_generator = message_generator
        self.wrapper = wrapper

    def __call__(self, exception, *args, **kwargs):
        message = self.message_generator(*args, **kwargs)
        raise self.wrapper(message)


class LogException(AbstractExceptionHandler):
    def __init__(self, message_generator):
        self.message_generator = message_generator

    def __call__(self, exception, *args, **kwargs):
        message = self.message_generator(exception, *args, **kwargs)
        log.log(message)


class HandlerContainer(object):
    def __init__(self, handlers):
        self.handlers = handlers

    def __call__(self, exception, *args, **kwargs):
        for handler in self.handlers:
            result = handler(exception, *args, **kwargs)
            if result:
                return result


def handle(handler):
    def decorator(f):
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as exception:
                return handler(exception, *args, **kwargs)
        return wrapper
    return decorator
