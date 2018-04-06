__disk_cache = None


def create_disk_cache(path='/tmp/cache/'):
    from diskcache import Cache
    global __disk_cache

    __disk_cache = Cache(path)
    return __disk_cache
