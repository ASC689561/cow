import sys


def is_debug()->bool:
    if 'pydevd' in sys.modules:
        return True
    else:
        return False
