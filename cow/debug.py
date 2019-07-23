import sys


def is_debug() -> bool:
    if 'pydevd' in sys.modules:
        return True
    else:
        return False


def is_docker() -> bool:
    with open('/proc/1/cgroup', 'rt') as ifh:
        return 'docker' in ifh.read()
