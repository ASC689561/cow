import logging
import os
from logging.handlers import RotatingFileHandler, SocketHandler

from logstash.formatter import LogstashFormatterBase


class CLogstashFormatterVersion1(LogstashFormatterBase):
    def __init__(self, message_type='Logstash', tags=None, fqdn=False, app_id='app_id'):
        super().__init__(message_type, tags, fqdn)
        self.app_id = app_id

    def format(self, record):
        # Create message dict
        message = {
            'app_id': self.app_id,
            '@timestamp': self.format_timestamp(record.created),
            '@version': '1',
            'message': record.getMessage(),
            'host': self.host,
            'path': record.pathname,
            'tags': self.tags,
            'type': self.message_type,

            # Extra Fields
            'level': record.levelname,
            'logger_name': record.name,
        }

        # Add extra fields
        message.update(self.get_extra_fields(record))

        # If exception, add debug info
        if record.exc_info:
            message.update(self.get_debug_fields(record))

        return self.serialize(message)


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
        self.formatter = CLogstashFormatterVersion1(message_type, tags, fqdn, app_id=app_id)

    def makePickle(self, record):
        return self.formatter.format(record) + b'\n'


class LogBuilder:
    def __init__(self):
        self.handlers = []
        self.format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    def build(self):
        logging.getLogger().handlers.clear()
        logging.basicConfig(level=logging.DEBUG, format=self.format_str, handlers=self.handlers)

    def set_format(self, format_str):
        self.format_str = format_str
        return self

    def init_stream_handler(self, level=logging.DEBUG):
        handler = logging.StreamHandler()
        self.handlers.append(handler)
        handler.setLevel(level)
        return self

    def init_rotating_file_stream_handler(self, log_path, level=logging.DEBUG):
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        debug_log = RotatingFileHandler(log_path + "/" + str(level) + ".log", maxBytes=5 * 1024 * 1024, mode='a',
                                        backupCount=10)
        debug_log.setLevel(level)
        self.handlers.append(debug_log)

    def init_rotating_file_handler(self, log_path, level=logging.DEBUG):
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        if level >= logging.DEBUG:
            debug_log = RotatingFileHandler(log_path + "/debug.log", maxBytes=5 * 1024 * 1024, mode='a', backupCount=10)
            debug_log.setLevel(logging.DEBUG)
            self.handlers.append(debug_log)

        if level >= logging.INFO:
            info_log = RotatingFileHandler(log_path + "/info.log", maxBytes=5 * 1024 * 1024, mode='a', backupCount=10)
            info_log.setLevel(logging.INFO)
            self.handlers.append(info_log)

        if level >= logging.ERROR:
            error_log = RotatingFileHandler(log_path + "/error.log", maxBytes=5 * 1024 * 1024, mode='a', backupCount=10)
            error_log.setLevel(logging.ERROR)
            self.handlers.append(error_log)

        if level >= logging.FATAL:
            fatal_log = RotatingFileHandler(log_path + "/fatal.log", maxBytes=5 * 1024 * 1024, mode='a', backupCount=10)
            fatal_log.setLevel(logging.FATAL)
            self.handlers.append(fatal_log)

        return self

    def init_logstash_handler(self, host, port, app_id, level=logging.ERROR):
        logstash_handler = CTCPLogstashHandler(host, port, app_id=app_id)
        logstash_handler.setLevel(level)
        self.handlers.append(logstash_handler)
        return self
