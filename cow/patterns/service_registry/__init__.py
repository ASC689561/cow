import json
import logging

import cow.patterns
from cow.patterns.singleton import Singleton


class ServiceRegistry:
    def register(self, service, endpoint):
        pass

    def get_service(self, service):
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
        svc_all = [endpoint]
        svc_all.extend(args)

        for v in svc_all:

            logging.info('Register service:' + v)

            if 'localhost' in v and 'server_ip' in os.environ:
                new_host = v.replace('localhost', os.environ['server_ip'])
                logging.info('Register service:' + new_host)
                self.zk_client.create(path, value=json.dumps({'service': service, 'endpoint': new_host}).encode(),
                                      ephemeral=True, sequence=True)

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

    def get_service(self, service):
        logging.info("get_service: {}".format(service))
        path = self._mpath('')
        svc = self.zk_client.get_children(path)

        all_service = []
        for v in svc:
            data, _ = self.zk_client.get(self._mpath(v))
            if data is None:
                continue
            json_obj = json.loads(data.decode())
            if service == json_obj.get('service', ''):
                all_service.append(json_obj['endpoint'])

        if cow.is_docker():
            for v in all_service:
                if 'localhost' not in v:
                    return v
        else:
            for v in all_service:
                if 'localhost' in v:
                    return v


if __name__ == '__main__':
    import cow
    import os

    os.environ['server_ip'] = '112.113.253.13'
    cow.LogBuilder().build()
    x = ZKServiceRegistry(zk_path='/test')
    x.register('db', 'http://localhost:9090', 'db:8001', 'http://abc:1212')
