#!/usr/bin/env python


import sys
import os
script_path  = "%s/yt3_scripts"%os.environ['HOME']
print script_path
sys.path.append(script_path)
import taxi
cwd=os.getcwd()
name = sys.argv[1]
this_taxi = taxi.taxi(dir=cwd, name = name)
this_taxi.save("%s/taxi_stand/%s"%(script_path,name))
#end
