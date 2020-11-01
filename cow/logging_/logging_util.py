import atexit
import logging
from logging.config import ConvertingList, ConvertingDict, valid_ident
from logging.handlers import QueueHandler, QueueListener
from queue import Queue

import yaml


def _resolve_handlers(l):
    if not isinstance(l, ConvertingList):
        return l

    return [l[i] for i in range(len(l))]


def _resolve_queue(q):
    if not isinstance(q, ConvertingDict):
        return q
    if '__resolved_value__' in q:
        return q['__resolved_value__']

    cname = q.pop('class')
    klass = q.configurator.resolve(cname)
    props = q.pop('.', None)
    kwargs = {k: q[k] for k in q if valid_ident(k)}
    result = klass(**kwargs)
    if props:
        for name, value in props.items():
            setattr(result, name, value)

    q['__resolved_value__'] = result
    return result


class QueueListenerHandler(QueueHandler):

    def __init__(self, handlers, respect_handler_level=False, auto_run=True, queue=Queue(-1)):
        queue = _resolve_queue(queue)
        super().__init__(queue)
        handlers = _resolve_handlers(handlers)
        self._listener = QueueListener(self.queue, *handlers, respect_handler_level=respect_handler_level)
        if auto_run:
            self.start()
            atexit.register(self.stop)

    def start(self):
        self._listener.start()

    def stop(self):
        self._listener.stop()

    def emit(self, record):
        return super().emit(record)


if __name__ == '__main__':
    logging_config = yaml.safe_load(open('./logconf.yaml'))

    logging.config.dictConfig(logging_config)

    print('------logger1--------')
    other_logger = logging.getLogger("logger1")
    other_logger.debug("debug")
    other_logger.info("info")
    other_logger.warning("warning")
    other_logger.exception("exception", exc_info=False)
    other_logger.error("error")
    other_logger.fatal("error")

    print('------logger2--------')
    other_logger = logging.getLogger("logger2")
    other_logger.debug("debug")
    other_logger.info("info")
    other_logger.warning("warning")
    other_logger.exception("exception", exc_info=False)
    other_logger.error("error")
    other_logger.fatal("error")

    print('------logger3--------')
    other_logger = logging.getLogger("logger3")
    other_logger.debug("debug")
    other_logger.info("info")
    other_logger.warning("warning")
    other_logger.exception("exception", exc_info=False)
    other_logger.error("error")
    other_logger.fatal("error")

    print('------root--------')
    other_logger = logging.getLogger()
    other_logger.debug("debug")
    other_logger.info("info")
    other_logger.warning("warning")
    other_logger.exception("exception", exc_info=False)
    other_logger.error("error")
    other_logger.fatal("error")

    print('------root--------')
    other_logger = logging.getLogger("slack")
    other_logger.debug("debug")
    other_logger.info("info")
    other_logger.warning("warning")
    other_logger.exception("exception", exc_info=False)
    other_logger.error("error")
    other_logger.fatal("error")
