def before(message_generator):
    def decorator(f):
        def wrapper(*args, **kwargs):
            message = message_generator(f, *args, **kwargs)
            print(message)
            result = f(*args, **kwargs)
            return result
        return wrapper
    return decorator


class M:
    @staticmethod
    def gen(f, obj, v):
        import dis
        print(f.__qualname__)


class A:
    @before(M.gen)
    def a(self, v):
        print(v)


a = A()
a.a(1)
