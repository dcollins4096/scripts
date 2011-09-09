#!/usr/bin/env python

fptr = open('OutputLog','r')
for n, line in enumerate(fptr):
    print n, line,
fptr.close
#end
