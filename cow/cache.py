disk_cache = None


def create_disk_cache(path='/tmp/cache/'):
    from diskcache import Cache
    global disk_cache

    disk_cache = Cache(path)
    return disk_cache
