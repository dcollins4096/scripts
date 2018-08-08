#!/usr/bin/env python
import sys
OutputLog = 'OutputLog'
if len(sys.argv) > 1:
    OutputLog = sys.argv[1]

fptr = open(OutputLog,'r')
lines = fptr.readlines()
fptr.close()
for n, line in enumerate(lines):
    print( n, line[:-1])
#end
