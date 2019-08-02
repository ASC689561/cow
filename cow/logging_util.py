import logging
import os
from logging.handlers import RotatingFileHandler

import requests


class LogBuilder:
    def __init__(self):
        self.handlers = []
        self.format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    def build(self):
        logging.getLogger().handlers.clear()
        logging.basicConfig(level=logging.DEBUG, handlers=self.handlers, format=self.format_str)

    def set_format(self, format_str):
        self.format_str = format_str
        return self

    def add_stream_handler(self, level=logging.DEBUG, format=None):
        handler = logging.StreamHandler()
        handler.setLevel(level)
        if format:
            handler.setFormatter(logging.Formatter(format))
        self.handlers.append(handler)
        return self

    def add_http_logstash_handler(self, host='http://logapi.misa.com.vn', port=80, app_id='test-log', system_id='test-log',
                                  level=logging.ERROR, database_path=None,
                                  headers=None):
        from logstash_async.handler import AsynchronousLogstashHandler
        from logstash_async.formatter import LogstashFormatter

        class HttpTransport:

            def __init__(self, host, port, **kwargs):
                self._host = host
                self._port = port
                self._headers = kwargs['headers'] if 'headers' in kwargs and kwargs['headers'] else {
                    'Authorization': 'Basic bWlzYTpNaXNhQDIwMTk=',
                    'Content-Type': 'application/json; charset=utf-8'}

            def close(self):
                pass

            def send(self, data: dict):
                try:
                    for v in data:
                        requests.post(url=self._host, data=v, headers=self._headers)
                except:
                    pass

        class CustomFormatter(LogstashFormatter):
            def _move_extra_record_fields_to_prefix(self, message):
                super()._move_extra_record_fields_to_prefix(message)
                message['app_id'] = app_id
                message['system_id'] = system_id

        handler = AsynchronousLogstashHandler(host, port, transport=HttpTransport(host, port, headers=headers),
                                              database_path=database_path)

        handler.formatter = CustomFormatter(tags=[app_id])
        handler.setLevel(level)
        self.handlers.append(handler)
        return self

    def add_rotating_file_handler(self, log_path, file_name='logging.log', level=logging.DEBUG, format=None):
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        handler = RotatingFileHandler(os.path.join(log_path, file_name), maxBytes=5 * 1024 * 1024, mode='a',
                                      backupCount=10)
        handler.setLevel(level)
        if format:
            handler.setFormatter(logging.Formatter(format))
        self.handlers.append(handler)
        return self

    def add_redis_handler(self, host, port, app_id, level=logging.ERROR):

        import logging
        import redis
        from logstash_async.formatter import LogstashFormatter

        class RedisHandler(logging.Handler):
            def __init__(self, host='localhost', port=6379):
                logging.Handler.__init__(self)

                self.r_server = redis.Redis(host, port)
                self.formatter = logging.Formatter("%(asctime)s - %(message)s")

            def emit(self, record):
                record.app_id = app_id
                self.r_server.rpush('log', self.format(record))

        class CustomFormatter(LogstashFormatter):
            def _move_extra_record_fields_to_prefix(self, message):
                message['app_id'] = app_id

        handler = RedisHandler(host, port)

        handler.formatter = CustomFormatter(tags=[app_id])
        handler.setLevel(level)
        self.handlers.append(handler)
        return self


if __name__ == '__main__':
    def init_log():
        bd = LogBuilder()
        bd.add_stream_handler(level=logging.DEBUG)
        bd.add_rotating_file_handler(log_path='/tmp/log', level=logging.WARNING)
        bd.add_http_logstash_handler(app_id='test-log', level=logging.INFO)
        bd.set_format("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        bd.build()


    init_log()

    logging.debug("debug")
    logging.info("Kiểm tra log tiếng việt")
    logging.warning("warning")
    logging.error("error")
    logging.critical("critical")
