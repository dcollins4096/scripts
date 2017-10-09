#!/usr/bin/env python


import sys
import os
script_path  = "%s/yt3_scripts"%os.environ['HOME']
print script_path
sys.path.append(script_path)
import taxi

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-l", "--like", dest="like",action="store",help = "width", default=None)
options, args = parser.parse_args()
#title=options.title
taxi_stand = "%s/taxi_stand/"%(script_path)
cwd=os.getcwd()
name = sys.argv[1]
if options.like != None:
    this_taxi = taxi.taxi("%s/%s"%(taxi_stand,options.like))
    this_taxi.directory = cwd
    this_taxi.name = name
    this_taxi.outname = name
else:
    this_taxi = taxi.taxi(dir=cwd, name = name)
this_taxi.save("%s/%s"%(taxi_stand,name))
#end
