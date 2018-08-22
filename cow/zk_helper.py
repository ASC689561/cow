import inspect
import json
import logging


def __zksingleton(cls):
    instances = {}

    def get_instance(*args):
        h = str(args)
        if h not in instances:
            instances[h] = cls(*args)
        return instances[h]

    return get_instance


@__zksingleton
class ZKHelper:
    def __init__(self, zk_client):
        self.zk_client = zk_client
        print(zk_client)

    def get_json(self, path) -> dict:
        try:
            data, _ = self.zk_client.get(path)
            if not data:
                return {}
            try:
                result = json.loads(data.decode())
            except:
                import yaml
                result = yaml.load(data.decode())

            return result or {}
        except:
            logging.exception(inspect.getargvalues(inspect.currentframe()), exc_info=True)
            return {}

    def get_ancestor_json(self, path):
        paths = path.split('/')
        data = {}
        for v in range(1, len(paths)):
            tmp_path = '/'.join(paths[0:v + 1])
            try:
                data.update(self.get_json(tmp_path))
            except:
                logging.exception(inspect.getargvalues(inspect.currentframe()), exc_info=True)
        return data
