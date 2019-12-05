import datetime
import logging
from contextlib import contextmanager
from timeit import default_timer

import ntplib
import pytz

init_time = None


@contextmanager
def Timer():
    start = default_timer()
    elapser = lambda: default_timer() - start
    yield lambda: elapser()
    end = default_timer()
    elapser = lambda: end - start


def get_ntp_time(time_zone='Asia/Ho_Chi_Minh') -> datetime.datetime:
    local_time_zone = pytz.timezone("Asia/Ho_Chi_Minh")  # time zone name from Olson database

    def get_time_from__ntp_client():
        logging.debug('Get time from ntp server')
        c = ntplib.NTPClient()
        response = c.request('pool.ntp.org', version=3)
        formatted_date_with_micro_seconds = datetime.datetime.strptime(
            str(datetime.datetime.utcfromtimestamp(response.tx_time)), "%Y-%m-%d %H:%M:%S.%f")
        local_dt = formatted_date_with_micro_seconds.replace(tzinfo=pytz.utc).astimezone(local_time_zone)
        formatted_date_with_corrections = str(local_dt).split("+")[0]
        return datetime.datetime.strptime(formatted_date_with_corrections, "%Y-%m-%d %H:%M:%S.%f")

    if time_zone not in init_time:
        try:
            time = get_time_from__ntp_client()
        except:
            return datetime.datetime.now()
        init_time[time_zone] = (datetime.datetime.now(), time)
    time_local, time_internet = init_time[time_zone]
    now = time_internet + datetime.timedelta(seconds=(datetime.datetime.now() - time_local).total_seconds())

    return now
