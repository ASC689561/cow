import os


def get_env_param(*list):
    t = []
    for v in list:
        if isinstance(v, tuple):
            t.append(os.environ.get(v[0], v[1]))
        elif isinstance(v, str):
            if v not in os.environ:
                raise Exception("{} not in env".format(v))
            t.append(os.environ[v])
        else:
            raise Exception("{} must be str or tuple".format(v))

    return tuple(t)
