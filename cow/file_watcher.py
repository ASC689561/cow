import os
import time
import _thread
import logging
import traceback


class Watcher(object):
    def __init__(self, file_name, callback):
        self.file_name = file_name
        self.callback = callback

    def thread(self):
        props = os.stat(self.file_name)
        this = props.st_size

        while 1:
            time.sleep(5)
            try:
                props = os.stat(self.file_name)
                if this != props.st_size:
                    logging.debug("file changed, old size: {}  new size: {}".format(this, props.st_size))
                    self.callback()
                    this = props.st_size
                    time.sleep(10)
            except:
                logging.error(traceback.format_exc())

    def start(self):
        logging.debug("Watching file:" + self.file_name)
        _thread.start_new_thread(self.thread, ())
