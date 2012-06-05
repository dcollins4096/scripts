#!/usr/bin/env python
import sys
OutputLog = 'OutputLog'
if len(sys.argv) > 1:
    OutputLog = sys.argv[1]

fptr = open(OutputLog,'r')
for n, line in enumerate(fptr):
    print n, line,
fptr.close
#end
