import logging
import os
from logging.handlers import RotatingFileHandler, SocketHandler


class CTCPLogstashHandler(SocketHandler, object):
    """Python logging handler for Logstash. Sends events over TCP.
    :param host: The host of the logstash server.
    :param port: The port of the logstash server (default 5959).
    :param message_type: The type of the message (default logstash).
    :param fqdn; Indicates whether to show fully qualified domain name or not (default False).
    :param version: version of logstash event schema (default is 0).
    :param tags: list of tags for a logger (default is None).
    """

    def __init__(self, host, port=5959, message_type='logstash', tags=None, fqdn=False, app_id='app_id'):
        super(CTCPLogstashHandler, self).__init__(host, port)
        from logstash import LogstashFormatterVersion1

        self.app_id = app_id
        self.formatter = LogstashFormatterVersion1(message_type, tags, fqdn)

    def makePickle(self, record):
        record.app_id = self.app_id
        return self.formatter.format(record) + b'\n'


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

    def add_logstash_handler(self, host, port, app_id, level=logging.ERROR):
        handler = CTCPLogstashHandler(host, port, app_id=app_id)
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