import functools
import logging
import time


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


def ignore_exception(time=3):
    def wrapped(func):
        @functools.wraps(func)
        def ignore(*args, **kw):
            for v in range(0, time):
                try:
                    result = func(*args, **kw)
                    return result
                except Exception as ex:
                    if v == time - 1:
                        raise ex

        return ignore

    return wrapped