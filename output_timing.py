#!/usr/bin/env python
import sys
import re

extra_re = re.compile(".*ED.._.....*")

def parse_level_write(fptr):
    counter = 0
    for line in fptr:
        if line.startswith('===  SMHD'):
            print line[:-1]
            continue
        if line.startswith('Extra Output'):
            print counter, line[:-1]
            counter += 1
            continue
        match=extra_re.match(line)
        if match:
            continue
        if line.startswith('WriteAllData'):
            print counter, line[:-1]
            counter += 1
            continue





try:
    filename = sys.argv[1]
except:
    filename = 'dump'

fptr = open(filename)
parse_level_write(fptr)

#end
