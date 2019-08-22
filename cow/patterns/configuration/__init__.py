import json
import logging
import os

from cow.patterns.singleton import Singleton


class ConfigBase:
    def get(self, key):
        pass

    def set(self, key, value):
        pass


class ZKConfigBase(ConfigBase, metaclass=Singleton):

    def __init__(self, zk_path='/config', zk_client=None):
        self.zk_path = zk_path
        self.zk_client = zk_client

        from kazoo.recipe.cache import TreeCache
        self.tree_cache = TreeCache(zk_client, zk_path)
        zk_client.start()
        self.zk_client.ensure_path(self.zk_path)
        self.tree_cache.start()
        while not self.tree_cache._is_initialized:
            logging.info("waiting tree init")
            import time
            time.sleep(1)

    def make_path(self, relative_path):
        return os.path.join(self.zk_path, relative_path)

    def get_json(self, relative_path=''):
        relative_path = self.make_path(relative_path)
        data = self.tree_cache.get_data(relative_path)
        return json.loads(data[1].decode())

    def get(self, key, path='', default=None):
        obj = self.get_json(self.make_path(path))
        return obj.get(key, default)

    def set(self, key, value, path=''):
        data = self.get_json(self.make_path(path))
        data[key] = value
        self.zk_client.set(self.make_path(path), json.dumps(data))

    def get_children(self, path):
        return self.tree_cache.get_children(self.make_path(path))
