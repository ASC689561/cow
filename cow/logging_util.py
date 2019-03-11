import logging
import os
from logging.handlers import RotatingFileHandler


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

    def add_redis_handler(self, host, port, app_id, level=logging.ERROR, database_path=None):

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

    def add_logstash_handler(self, host, port, app_id, level=logging.ERROR, database_path=None):
        from logstash_async.handler import AsynchronousLogstashHandler
        from logstash_async.formatter import LogstashFormatter

        class CustomFormatter(LogstashFormatter):
            def _move_extra_record_fields_to_prefix(self, message):
                super()._move_extra_record_fields_to_prefix(message)
                message['app_id'] = app_id

        handler = AsynchronousLogstashHandler(host, port, database_path=database_path or f'/tmp/logstash_{app_id}.db')

        handler.formatter = CustomFormatter(tags=[app_id])
        handler.setLevel(level)
        self.handlers.append(handler)
        return self


if __name__ == '__main__':
    def init_log():
        bd = LogBuilder()
        bd.add_stream_handler(level=logging.DEBUG)
        bd.add_rotating_file_handler(log_path='.', level=logging.WARNING)
        bd.add_logstash_handler(host='117.6.16.176', port=91, app_id='test', level=logging.WARNING)
        bd.set_format("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        bd.build()


    init_log()

    logging.debug("debug")
    logging.info("info")
    logging.warning("warning")
    logging.error("error")
    logging.critical("critical")
