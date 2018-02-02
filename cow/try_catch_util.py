import logging


def catch_exception(exception=Exception, default_value=None, logger=logging.getLogger(__name__)):
    def deco(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except exception as err:
                logger.exception(err)
                return default_value
            else:
                return result

        return wrapper

    return deco


if __name__ == "__main__":
    @catch_exception(FileExistsError, default_value=1, logger=logging.getLogger('test'))
    def exception():
        return 1 / 0


    print(exception())
