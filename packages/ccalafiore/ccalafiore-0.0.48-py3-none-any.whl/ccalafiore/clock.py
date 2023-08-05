import time as tm
import datetime
from . import maths


hours_per_day = 24
minutes_per_hour = 60
minutes_per_day = hours_per_day * minutes_per_hour
seconds_per_minute = 60
seconds_per_hour = minutes_per_hour * seconds_per_minute
seconds_per_day = hours_per_day * seconds_per_hour
milliseconds_per_second = 1000
milliseconds_per_minute = milliseconds_per_second * seconds_per_minute
milliseconds_per_hour = milliseconds_per_minute * minutes_per_hour
milliseconds_per_day = milliseconds_per_hour * hours_per_day
microseconds_per_millisecond = 1000
microseconds_per_second = microseconds_per_millisecond * milliseconds_per_second
microseconds_per_minute = microseconds_per_second * seconds_per_minute
microseconds_per_hour = microseconds_per_minute * minutes_per_hour
microseconds_per_day = microseconds_per_hour * hours_per_day


class SecTimer:

    def __init__(self):
        self.end = None
        self.delta = None
        self.start = tm.time()

    def get_seconds(self):
        self.end = tm.time()
        self.delta = self.end - self.start

        return self.delta

    def to_milliseconds(self):
        self.end = tm.time()
        self.delta = self.end - self.start

        milliseconds = self.delta * milliseconds_per_second
        return milliseconds


class AllUnitsTimer:
    def __init__(self):
        self.end = None
        self.delta = None
        self.start = datetime.datetime.today()

    def get_all_unit_time(self):
        self.end = datetime.datetime.today()
        timedelta = self.end - self.start
        self.delta = AllUnitTime(days=timedelta.days, seconds=timedelta.seconds, microseconds=timedelta.microseconds)
        return self.delta

    def get_seconds(self):
        self.end = datetime.datetime.today()
        timedelta = self.end - self.start
        self.delta = AllUnitTime(days=timedelta.days, seconds=timedelta.seconds, microseconds=timedelta.microseconds)
        seconds = self.delta.to_seconds()
        return seconds

    def get_milliseconds(self):
        self.end = datetime.datetime.today()
        timedelta = self.end - self.start
        self.delta = AllUnitTime(days=timedelta.days, seconds=timedelta.seconds, microseconds=timedelta.microseconds)
        milliseconds = self.delta.to_milliseconds()
        return milliseconds


class AllUnitTime:
    def __init__(self, days=0, hours=0, minutes=0, seconds=0, milliseconds=0, microseconds=0):
        self.type = 'day'

        self.microseconds = maths.convert_to_int_or_float(
            (maths.convert_to_int_or_float(days) * microseconds_per_day) +
            (maths.convert_to_int_or_float(hours) * microseconds_per_hour) +
            (maths.convert_to_int_or_float(minutes) * microseconds_per_minute) +
            (maths.convert_to_int_or_float(seconds) * microseconds_per_second) +
            (maths.convert_to_int_or_float(milliseconds) * microseconds_per_millisecond) +
            maths.convert_to_int_or_float(microseconds))

        self.milliseconds = int(self.microseconds / microseconds_per_millisecond)
        self.microseconds -= (self.milliseconds * microseconds_per_millisecond)

        self.seconds = int(self.milliseconds / milliseconds_per_second)
        self.milliseconds -= (self.seconds * milliseconds_per_second)

        self.minutes = int(self.seconds / seconds_per_minute)
        self.seconds -= (self.minutes * seconds_per_minute)

        self.hours = int(self.minutes / minutes_per_hour)
        self.minutes -= (self.hours * minutes_per_hour)

        self.days = int(self.hours / hours_per_day)
        self.hours -= (self.days * hours_per_day)

    def to_seconds(self):

        seconds = (
            (self.days * seconds_per_day) +
            (self.hours * seconds_per_hour) +
            (self.minutes * seconds_per_minute) +
            self.seconds +
            maths.convert_to_int_or_float(self.milliseconds / milliseconds_per_second) +
            maths.convert_to_int_or_float(self.microseconds / microseconds_per_second))

        return seconds

    def to_milliseconds(self):

        milliseconds = (
            (self.days * milliseconds_per_day) +
            (self.hours * milliseconds_per_hour) +
            (self.minutes * milliseconds_per_minute) +
            (self.seconds * milliseconds_per_second) +
            self.milliseconds +
            maths.convert_to_int_or_float(self.microseconds / microseconds_per_second))

        return milliseconds
