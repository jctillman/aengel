from datetime import datetime

def get_time_in_minutes_from_str(str_time):
    hour, minute = str_time.split(":")
    return int(hour) * 60 + int(minute)

def get_time_in_minutes():
    now = datetime.now()
    return now.hour * 60 + now.minute

def timing_within_interval(timing):
    start_time = get_time_in_minutes_from_str(timing['time_start'])
    end_time = get_time_in_minutes_from_str(timing['time_end'])
    current_time = get_time_in_minutes()
    return start_time <= current_time and end_time >= current_time