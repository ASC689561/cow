def ensure_directory_exists(path):
    import os
    if not os.path.exists(path):
        os.makedirs(path)


def get_callee_path():
    import os, inspect
    return os.path.dirname(os.path.abspath(inspect.stack()[1][1]))
