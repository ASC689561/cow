"""Decorator to create lazy attributes."""


class LazyWrapper(object):
    def __init__(self, func):
        self.func = func

    def __call__(self):
        try:
            return self.value
        except AttributeError:
            self.value = self.func()
            return self.value


class LazyProperty(object):

    def __init__(self, func):
        self._func = func
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, obj, klass=None):
        if obj is None: return None
        result = obj.__dict__[self.__name__] = self._func(obj)
        return result
