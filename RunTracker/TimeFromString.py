from datetime import tzinfo, timedelta, datetime
import time as _time

import sys
ZERO = timedelta(0)
HOUR = timedelta(hours=1)

# A class capturing the platform's idea of local time.

def make4digits(year):
    if year > 1900:
        return year
    if year > 70:
        return year+1900
    else:
        return year + 2000

STDOFFSET = timedelta(seconds = _time.timezone)
if _time.daylight:
    DSTOFFSET = timedelta(seconds = _time.altzone)
else:
    DSTOFFSET = STDOFFSET

DSTDIFF = DSTOFFSET - STDOFFSET

class LocalTimezone(tzinfo):

    def utcoffset(self, dt):
        if self._isdst(dt):
            return DSTOFFSET
        else:
            return STDOFFSET

    def dst(self, dt):
        if self._isdst(dt):
            return DSTDIFF
        else:
            return ZERO

    def tzname(self, dt):
        return _time.tzname[self._isdst(dt)]

    def _isdst(self, dt):
        tt = (dt.year, dt.month, dt.day,
              dt.hour, dt.minute, dt.second,
              dt.weekday(), 0, -1)
        stamp = _time.mktime(tt)
        tt = _time.localtime(stamp)
        return tt.tm_isdst > 0

Local = LocalTimezone()

import datetime
def TimeFromString(TimeString):
    if TimeString == "now":
        Time = datetime.datetime.utcnow()
    else:
        Array = TimeString.split(" ")
        if len(Array) == 4:
            year =  int(Array[0])
            month = int(Array[1])
            day =   int(Array[2])
            time =  Array[3]
        elif len(Array) == 3:
            year = datetime.date.today().year
            month = int(Array[0])
            day =   int(Array[1])
            time =  Array[2]
        elif len(Array) == 2:
            date = Array[0].split("/")
            year = make4digits( int(date[2]) )
            month = int(date[0])
            day = int(date[1])
            time =  Array[1]
        else:
            print 'Acceptable formats: all converted to UTC from machine local.'
            print 'yyyy mm dd tt:tt'
            print 'mm/dd/yy tt:tt'
            print 'mm dd tt:tt (year assumed to be current)'
            sys.exit(1)

        hour = int( time.split(":")[0] )
        min =  int( time.split(":")[1] )

        Time = datetime.datetime(year,month, day, hour, min)
        Time = Time + Local.utcoffset(Time)

    return Time.isoformat() #Output


