#!/usr/bin/env python
import sys
name = sys.argv[1]

sp = name.split(".")
for ext in ['eps','png','pdf']:
    if ext in sp:
        print 0

print 1
#end

