import json
import logging
import os

import cow
import cow.patterns
from cow.patterns.singleton import Singleton


class ServiceRegistry:
    def register(self, service, endpoint):
        pass

    def get_service(self, service, wait=True):
        pass


class ZKServiceRegistry(ServiceRegistry, metaclass=Singleton):

    def __init__(self, zk_path='/services', zk_client=None):
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

    def _mpath(self, relative_path):
        return os.path.join(self.zk_path, relative_path)

    def register(self, service, endpoint):
        path = self._mpath(service)
        self.zk_client.create(path, value=json.dumps({'service': service, 'endpoint': endpoint}).encode(), ephemeral=True, sequence=True)

    def export_env(self):
        path = self._mpath('')
        svc = self.zk_client.get_children(path)
        all_service = set()

        for v in svc:
            data, _ = self.zk_client.get(self._mpath(v))
            if data is None:
                continue
            json_obj = json.loads(data.decode())
            all_service.add(json_obj.get('service', ''))

        for s in all_service:
            if s:
                value = self.get_service(s)
                logging.info("Export {}={} to env".format(s, value))
                os.environ[s] = value

    def get_service(self, service, wait=True):

        path = self._mpath('')
        svc = self.zk_client.get_children(path)
        while True:

            all_service = []
            for v in svc:
                data, _ = self.zk_client.get(self._mpath(v))
                if data is None:
                    continue
                json_obj = json.loads(data.decode())
                if service == json_obj.get('service', ''):
                    all_service.append(json_obj['endpoint'])

            result = None

            if not all_service:
                result = None
            else:
                is_docker = cow.is_docker()

                for v in all_service:
                    if is_docker and 'localhost' not in v:
                        result = v
                    if not is_docker and 'localhost' in v:
                        result = v
            if not wait or result:
                return result
            logging.warning("Waiting for service: " + service)
            import time
            time.sleep(1)


if __name__ == '__main__':
    x = ZKServiceRegistry(zk_path='/test')
    z.export_env()
