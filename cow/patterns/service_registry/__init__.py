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
        if zk_client is None:
            from kazoo.client import KazooClient
            zk_client = KazooClient(os.environ.get('ZOOKEEPER', 'localhost:2181'))

        zk_client.restart()
        self.zk_path = zk_path
        self.zk_client = zk_client

        from kazoo.recipe.cache import TreeCache
        self.tree_cache = TreeCache(zk_client, zk_path)
        self.zk_client.ensure_path(self.zk_path)
        self.tree_cache.start()
        while not self.tree_cache._is_initialized:
            logging.info("waiting tree init")
            import time
            time.sleep(1)

    def _mpath(self, relative_path):
        return os.path.join(self.zk_path, relative_path)

    def register(self, service, endpoint, *args):
        path = self._mpath(service)
        self.zk_client.create(path, value=json.dumps({'service': service, 'endpoint': endpoint}).encode(),
                              ephemeral=True, sequence=True)
        for v in args:
            self.zk_client.create(path, value=json.dumps({'service': service, 'endpoint': v}).encode(),
                                  ephemeral=True, sequence=True)

    def export_env(self, service, *args):

        services = {service}
        services.update(args)
        logging.info("export_env: {}".format(str(services)))

        for s in services:
            if s:
                value = self.get_service(s)
                logging.info("Export {}={} to env".format(s, value))
                os.environ[s] = value

    def get_service(self, service, wait=False):
        logging.info("get_service: {}".format(service))

        path = self._mpath('')
        logging.info("x")
        logging.info( str(self.zk_client.hosts))
        logging.info( path)
        svc = self.zk_client.get_children(path)
        logging.info("a")

        times = 10
        while times >= 0:
            logging.info(times)
            logging.info("b")

            times -= 1

            all_service = []
            for v in svc:
                logging.info("aa")

                data, _ = self.zk_client.get(self._mpath(v))
                if data is None:
                    continue
                logging.info("axx")

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
            logging.error("Waiting for service: " + service)
            import time
            time.sleep(1)


if __name__ == '__main__':
    x = ZKServiceRegistry(zk_path='/test')
    z.export_env()
