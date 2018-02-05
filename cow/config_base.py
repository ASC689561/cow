import logging
import os


class ConfigBase:

    def __init__(self):
        pass

    def merge_dic(self, dic):
        for k, v in dic.items():
            setattr(self, k, v)

    def merge_env(self, *list_property_name):
        self_attr_dic = list(self._get_all_attr())
        if len(list_property_name) == 0:
            for v in self_attr_dic:
                if v in os.environ:
                    setattr(self, v, os.environ[v])
        else:
            for v in list_property_name:
                if v not in self_attr_dic:
                    raise Exception("Property {} not in attribute of config".format(v))
                if v in os.environ:
                    try:
                        setattr(self, v, os.environ[v])
                    except:
                        logging.error("Error while try set atribute: {}".format(v))

    def __str__(self):
        import json
        return json.dumps(self.__dict__, indent=4)

    def _get_all_attr(self):
        attr = dir(self)
        for v in attr:
            if str.startswith(v, '__'):
                continue
            yield v
