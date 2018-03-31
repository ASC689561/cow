import sys


def is_debug():
    if 'pydevd' in sys.modules:
        return True
    else:
        return False


def execute_from(string):
    import inspect
    for v in inspect.stack():
        if v.function == string:
            return True
    return False
