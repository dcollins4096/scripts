#!/usr/bin/env python
import sys
import TimeFromString

print "<StartTime>",TimeFromString.TimeFromString(sys.argv[1]),"</StartTime>"
print "<EndTime>",TimeFromString.TimeFromString(sys.argv[2]),"</EndTime>"
#end
