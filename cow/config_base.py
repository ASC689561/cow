import logging
import os
import signal
import threading


class ConfigBase:

    def __init__(self):
        pass

    def merge_dic(self, dic):
        for k, v in dic.items():
            setattr(self, k, v)

    def merge_zk(self, zk_server, config_path, monitor_path=None, auto_terminated=True):
        from kazoo.client import KazooClient
        sleepEvent = threading.Event()

        zk = KazooClient(hosts=zk_server)
        zk.start()

        @zk.DataWatch(config_path)
        def watch_node(data, stat):
            logging.warning("Config chagned")

            import json
            if sleepEvent.is_set() and auto_terminated:
                logging.warning("Config chagned, Auto terminated app.")
                os.kill(os.getpid(), signal.SIGTERM)
            dic = json.loads(data.decode("utf-8"))
            self.merge_dic(dic)
            sleepEvent.set()

        def heartbeat():
            zk.create(monitor_path, b'', ephemeral=True, makepath=True)

            while True:
                import time
                time.sleep(5)
                import datetime
                zk.set(monitor_path, str(datetime.datetime.now()).encode())
                logging.debug('heartbeat')

        sleepEvent.wait()
        if monitor_path:
            t = threading.Thread(target=heartbeat, args=())
            t.start()

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
