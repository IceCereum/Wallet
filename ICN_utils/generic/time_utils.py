from datetime import datetime, timezone

def time_now():
    return str(datetime.now())

def utc_to_local(utc_dt):
    return datetime.strptime(utc_dt, "%Y-%m-%d %H:%M:%S.%f").                  \
                                replace(tzinfo=timezone.utc).astimezone(tz=None)