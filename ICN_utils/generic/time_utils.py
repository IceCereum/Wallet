from datetime import datetime, timezone

def time_now():
    return str(datetime.now())

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)