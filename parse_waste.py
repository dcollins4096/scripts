#!/usr/bin/env python
""" Parses the waste log.
If run on the command line, reports the total time today."""


import sys
import datetime as dt
filename = '/Users/dcollins/Sites/Research/CodeGames/WasteingAway/waste_data'

def parse(debug = 0):
    file = open(filename)
    time_today = 0
    history = {}
    today = dt.date.today()
    month_lookup = {'Jan':1,'Feb':2,'Mar':3,'Apr':4, 'May':5, 'Jun':6,\
                    'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}

    counter = 0
    try:
        for line in file:
            #Tue Jan  5 13:47:13 PST 2010
            arg = line.split(" ")
            date = []
            for a in arg:
                if a != "":
                    date.append(a)
            if debug > 2:
                print date
            month = int(month_lookup[date[1]])
            day  = int(date[2])
            time = date[3]
            year = int(date[5])
            time = time.split(":")
            history.setdefault(year,{})
            hyear = history[year]
            hyear.setdefault(month,{})
            hmonth = hyear[month]
            hmonth.setdefault(day,0)
            hmonth[day] += 1
            if debug > 1:
                print today.day, day
                print today.month, month
                print today.year, year
            
            if day == today.day and\
                   month == today.month and\
                   year == today.year:
                if debug > 0:
                    print "Got one!", date
                time_today += 1
    except:
        raise
    finally:
        file.close()
    timer_cadence = 30
    minutes = time_today * timer_cadence / 60.0
    print "Wasted ", minutes, "minutes today"
if __name__ == '__main__':
    import sys
    debug = 0
    if len(sys.argv) > 1:
        debug = sys.argv[1]
    parse(debug)
#end
