import logging
import os
from logging.handlers import RotatingFileHandler
import colorlog
import requests


class LogBuilder:
    def __init__(self):
        self.handlers = []
        self.format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    def build(self):
        logging.getLogger().handlers.clear()
        logging.basicConfig(level=logging.DEBUG, format=self.format_str)
        logging.getLogger().handlers.extend(self.handlers)

    def add_stream_handler(self, level=logging.DEBUG, format=None):
        handler = logging.StreamHandler()
        handler.setLevel(level)
        if format:
            handler.setFormatter(logging.Formatter(format))
        self.handlers.append(handler)
        return self

    def add_stream_color_handler(self, level=logging.DEBUG, format=None):
        handler =  colorlog.StreamHandler()

        handler.setLevel(level)
        if format:
            handler.setFormatter(logging.Formatter(format))
        else:
            handler.setFormatter(colorlog.ColoredFormatter(
                '%(log_color)s%(levelname)s:%(name)s:%(message)s'))
        self.handlers.append(handler)
        return self

    def add_http_logstash_handler(self, host='http://logapi.misa.com.vn',
                                  port=80, app_id='test-log', system_id='test-log', level=logging.ERROR, headers=None):
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

            def send(self, data: dict, use_logging=None):
                for v in data:
                    res = requests.post(url=self._host, data=v, headers=self._headers)

        class CustomFormatter(LogstashFormatter):
            def _move_extra_record_fields_to_prefix(self, message):
                super()._move_extra_record_fields_to_prefix(message)
                message['app_id'] = app_id
                message['system_id'] = system_id

        handler = AsynchronousLogstashHandler(host, port, transport=HttpTransport(host, port, headers=headers),
                                              database_path=None)

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

    def add_redis_handler(self, redis_url, app_id, system_id, log_key='log_queue', level=logging.ERROR, redis_ttl=86400):

        import logging
        from redis import StrictRedis
        from logstash_async.formatter import LogstashFormatter

        class CustomFormatter(LogstashFormatter):
            def _move_extra_record_fields_to_prefix(self, message):
                super()._move_extra_record_fields_to_prefix(message)
                message['app_id'] = app_id
                message['system_id'] = system_id

        class RedisKeyHandler(logging.StreamHandler):
            def __init__(self, key: str, ttl: int = None, **kwargs):
                super().__init__(**kwargs)
                self.redis_client = StrictRedis.from_url(redis_url)
                self.key = key
                self.ttl = ttl

                if self.ttl:
                    self.redis_client.expire(self.key, self.ttl)

            def emit(self, message: logging.LogRecord):
                data = formatter.format(message)
                self.redis_client.rpush(self.key, data)

        formatter = CustomFormatter()
        redis_handler = RedisKeyHandler(key=log_key, ttl=redis_ttl)
        redis_handler.setLevel(level)
        self.handlers.append(redis_handler)
        return self


if __name__ == '__main__':
    def init_log():
        bd = LogBuilder()
        # bd.add_stream_handler(level=logging.DEBUG)
        bd.add_stream_color_handler(level=logging.DEBUG)
        bd.add_rotating_file_handler(log_path='/tmp/log', level=logging.WARNING)
        bd.add_http_logstash_handler(app_id='test-log', level=logging.INFO)
        bd.build()


    init_log()

    logging.debug("debug")
    logging.info("Kiểm tra log tiếng việt")
    logging.warning("warning")
    logging.error("error")
    logging.critical("critical")
