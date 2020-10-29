import contextlib


@contextlib.contextmanager
def ignore_exception():
    try:
        yield
    except:
        pass
