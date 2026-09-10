import time
DAYS_IN_MONTH = [None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
def is_leap(year: int):
    if not isinstance(year, int):    raise TypeError
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
def days_in_month(year: int, month: int):
    if not isinstance(year, int):    raise TypeError
    if not isinstance(month, int):    raise TypeError
    if not (1 <= month <= 12):    raise ValueError
    if month == 2 and is_leap(year):
        return 29
    return DAYS_IN_MONTH[month]
def now():
    timestamp = time.time()
    time_tuple = time.localtime(timestamp)
    fractional_seconds = timestamp - int(timestamp)
    return TimeClock(
        year=time_tuple.tm_year,
        month=time_tuple.tm_mon,
        day=time_tuple.tm_mday,
        hour=time_tuple.tm_hour,
        minute=time_tuple.tm_min,
        second=time_tuple.tm_sec,
        milliseconds=int(fractional_seconds * 1000),
        nanoseconds=int(fractional_seconds * 1e9) % 1000
    )
class Time:
    def __init__(self, hour = 0, minute = 0, second = 0, milliseconds = 0, nanoseconds = 0):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.milliseconds = milliseconds
        self.nanoseconds = nanoseconds
    def __repr__(self):
        return f"Time(hour={self.hour}, minute={self.minute}, second={self.second}, milliseconds={self.milliseconds}, nanoseconds={self.nanoseconds})"
    def __str__(self):
        return f"{self.hour}:{self.minute}:{self.second:02d}.{self.milliseconds:03d}{self.nanoseconds:03d}"
class Date:
    def __init__(self, year = 1, month = 1, day = 1):
        self.year = year
        self.month = month
        self.day = day
    def __repr__(self):
        return f"Date(year={self.year}, month={self.month}, day={self.day})"
    def __str__(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d}"
class TimeClock:
    def __init__(self, year = 1, month = 1, day = 1, hour = 0, minute = 0, second = 0, milliseconds = 0, nanoseconds = 0):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.milliseconds = milliseconds
        self.nanoseconds = nanoseconds
    def __repr__(self):
        return f"TimeClock(year={self.year}, month={self.month}, day={self.day}, hour={self.hour}, minute={self.minute}, second={self.second}, milliseconds={self.milliseconds}, nanoseconds={self.nanoseconds})"
    def __str__(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d} {self.hour}:{self.minute}:{self.second:02d}.{self.milliseconds:03d}{self.nanoseconds:03d}"