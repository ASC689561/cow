import functools
import logging
import time
import os

from contextlib import contextmanager
import threading
import _thread


def timing(func=None, name=None, log_level=logging.DEBUG):
    def timing(f):
        def wrap(*args):
            time1 = time.time()
            ret = f(*args)
            time2 = time.time()
            log_time = (time2 - time1) * 1000.0

            if func is None:
                logging.log(log_level, '%s function took %0.3f ms' % (f.__name__, log_time),
                            extra={f.__name__: str(log_time)})
            else:
                if name is None:
                    func(f.__name__, log_time, *args)
                else:
                    func(name, log_time, *args)
            return ret

        return wrap

    return timing


def ignore_exception(times=1, reraise=True):
    """
    Retry and Ignore exception
    :param time: times to retry
    :param reraise: Reraise exception if True
    """

    def wrapped(func):
        @functools.wraps(func)
        def ignore(*args, **kw):
            for v in range(0, times):
                try:
                    result = func(*args, **kw)
                    return result
                except Exception as ex:
                    logging.exception(ex)
                    if v == times - 1:
                        if reraise:
                            raise ex

        return ignore

    return wrapped


def execute_if_env(env):
    def wrapped(func):
        @functools.wraps(func)
        def ignore(*args, **kw):
            if os.environ.get(env, 'False').lower() == 'true':
                result = func(*args, **kw)
                return result
            return None

        return ignore

    return wrapped


class TimeoutException(Exception):
    def __init__(self, msg=''):
        self.msg = msg


@contextmanager
def time_limit(seconds, msg=''):
    timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
    timer.start()
    try:
        yield
    except KeyboardInterrupt:
        raise TimeoutException("Timed out for operation {}".format(msg))
    finally: 
        timer.cancel()


if __name__ == '__main__':
    @execute_if_env('TEST')
    def xx():
        print('xx')


    os.environ['TEST'] = 'true'
    xx()

    import time

    # ends after 5 seconds
    with time_limit(5, 'sleep'):
        for i in range(10):
            time.sleep(1)

    # this will actually end after 10 seconds
    with time_limit(5, 'sleep'):
        time.sleep(10)
