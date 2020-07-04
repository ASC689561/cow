import datetime
import logging
import threading

import ntplib
import pytz

_lock = threading.Lock()
init_time = {}


def get_ntp_time(time_zone='Asia/Ho_Chi_Minh') -> datetime.datetime:
    global init_time
    local_time_zone = pytz.timezone(time_zone)  # time zone name from Olson database

    if time_zone not in init_time:
        try:
            with _lock:
                logging.debug('Get time from ntp server')
                c = ntplib.NTPClient()
                response = c.request('pool.ntp.org', version=3)
                formatted_date_with_micro_seconds = datetime.datetime.strptime(
                    str(datetime.datetime.utcfromtimestamp(response.tx_time)), "%Y-%m-%d %H:%M:%S.%f")
                local_dt = formatted_date_with_micro_seconds.replace(tzinfo=pytz.utc).astimezone(local_time_zone)
                formatted_date_with_corrections = str(local_dt).split("+")[0]
                ntp_time = datetime.datetime.strptime(formatted_date_with_corrections, "%Y-%m-%d %H:%M:%S.%f")
                init_time[time_zone] = (datetime.datetime.now(), ntp_time)
        except:
            init_time[time_zone] = (datetime.datetime.now(), datetime.datetime.now())
    time_local, time_internet = init_time[time_zone]
    now = time_internet + datetime.timedelta(seconds=(datetime.datetime.now() - time_local).total_seconds())
    return now


if __name__ == '__main__':
    from cow import LogBuilder

    bd = LogBuilder()
    bd.add_stream_color_handler(level=logging.DEBUG)
    bd.build()

    for v in range(100):
        t = get_ntp_time(time_zone='UTC')
        print(t)
