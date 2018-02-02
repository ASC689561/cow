import sys


def is_debug():
    if 'pydevd' in sys.modules:
        return True
    else:
        return False
