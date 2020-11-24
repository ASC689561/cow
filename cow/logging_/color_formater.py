import colorlog
from .elk_handler import FORMATTER_RECORD_FIELD_SKIP_LIST


class ColoredFormatter(colorlog.ColoredFormatter):

    def __init__(self, fmt=None, datefmt=None, style='%',
                 log_colors=None, reset=True,
                 secondary_log_colors=None, show_extra=False):
        super(ColoredFormatter, self).__init__(fmt, datefmt, style, log_colors, reset, secondary_log_colors)
        self.show_extra = show_extra

    def format(self, record):
        m = str(record.msg)
        old_message = m

        if not m.endswith(']  '):
            extra_txt = {}
            for k, v in record.__dict__.items():
                if k not in FORMATTER_RECORD_FIELD_SKIP_LIST:
                    extra_txt[k] = v
            if len(extra_txt) > 0:
                record.msg = m + " [" + str(extra_txt) + "]  "

        formatted = super().format(record)
        record.msg = old_message
        return formatted
