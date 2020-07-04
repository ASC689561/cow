"""Decorator to create lazy attributes."""


class LazyProperty(object):
    """
    class LazyClass:
        @LazyProperty
        def value(self):
            print('calculate value')
            return 1
    """

    def __init__(self, func):
        self._func = func
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, obj, klass=None):
        if obj is None: return None
        result = obj.__dict__[self.__name__] = self._func(obj)
        return result


class LazyClass:
    @LazyProperty
    def value(self):
        print('calculate value')
        return 1


if __name__ == '__main__':
    x = LazyClass()
    print(x.value)
    print(x.value)
    print(x.value)
    x.__dict__.pop('value')
    x.value.clear()
