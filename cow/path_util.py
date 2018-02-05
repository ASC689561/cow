import inspect
import os


def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_callee_path():
    return os.path.dirname(os.path.abspath(inspect.stack()[1][1]))
