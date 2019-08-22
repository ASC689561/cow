import inspect

__all__ = ['on', 'when']


def on(param_name):
    def f(fn):
        dispatcher = Dispatcher(param_name, fn)
        return dispatcher

    return f


def when(param_type):
    def f(fn):
        frame = inspect.currentframe().f_back
        func_name = fn.func_name if 'func_name' in dir(fn) else fn.__name__
        dispatcher = frame.f_locals[func_name]
        if not isinstance(dispatcher, Dispatcher):
            dispatcher = dispatcher.dispatcher
        dispatcher.add_target(param_type, fn)

        def ff(*args, **kw):
            return dispatcher(*args, **kw)

        ff.dispatcher = dispatcher
        return ff

    return f


class Dispatcher(object):
    def __init__(self, param_name, fn):
        frame = inspect.currentframe().f_back.f_back
        top_level = frame.f_locals == frame.f_globals
        self.param_index = self.__argspec(fn).args.index(param_name)
        self.param_name = param_name
        self.targets = {}

    def __call__(self, *args, **kw):
        typ = args[self.param_index].__class__
        d = self.targets.get(typ)
        if d is not None:
            return d(*args, **kw)
        else:
            issub = issubclass
            t = self.targets
            ks = t.iterkeys()
            return [t[k](*args, **kw) for k in ks if issub(typ, k)]

    def add_target(self, typ, target):
        self.targets[typ] = target

    @staticmethod
    def __argspec(fn):
        # Support for Python 3 type hints requires inspect.getfullargspec
        return inspect.getfullargspec(fn)


if __name__ == '__main__':

    import visitor


    class Person(object):
        def __init__(self, name):
            self.name = name

        def accept(self, visitor):
            visitor.visit(self)


    class Pet(object):
        def __init__(self, name, breed):
            self.name = name
            self.breed = breed

        def accept(self, visitor):
            visitor.visit(self)


    class DescendantsVisitor(object):
        def __init__(self):
            self.level = 0

        @visitor.on('member')
        def visit(self, member):
            pass

        @visitor.when(Person)
        def visit(self, member):
            print('person')

        @visitor.when(Pet)
        def visit(self, member):
            print('Pet')


    v = DescendantsVisitor()

    arr = [Pet('abc', 'def'), Person('abc'), Pet('abc', 'def')]

    for item in arr:
        item.accept(v)
