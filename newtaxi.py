#!/usr/bin/env python

import sys
import glob
import os


from optparse import OptionParser
parser = OptionParser()
parser.add_option("-l", "--like", dest="like",action="store",help = "width", default=None)
parser.add_option("-p", "--python", dest="python",action="store",help = "python 2 or 3. Default 2 ", default=2)
options, args = parser.parse_args()
using_taxi = False

if options.python == 2:
    script_path  = "%s/ytscripts"%os.environ['HOME']
else:
    script_path  = "%s/yt_33"%os.environ['HOME']
print(script_path)

if using_taxi:
    sys.path.append(script_path)
    import taxi
#title=options.title
taxi_stand = "%s/taxi_stand/"%(script_path)
cwd=os.getcwd()
name = sys.argv[1]
like_this_name  = None
if options.like != None:
    like_this_name = "%s/%s"%(taxi_stand,options.like)

if using_taxi:
    this_taxi = taxi.taxi(like_this_name)
    this_taxi.directory = cwd
    this_taxi.name = name
    this_taxi.outname = name
    this_taxi.save("%s/%s"%(taxi_stand,name))
else:
    lines = []
    lines.append( "self.name = '%s'\n"%name  )
    lines.append( "self.directory = '%s'\n"%cwd  )
    lines.append( "self.outname = '%s'\n"%name  )
    new_var = ['name','directory','outname']
    if options.like != None:
        if glob.glob(like_this_name) != []:
            other_file = open(like_this_name,'r')
            for line in other_file:
                clone=True
                for var in new_var:
                    check = "self.%s "%var
                    if line.startswith(check):
                        clone=False
                if clone:
                    lines.append(line)
        else:
            print( "No such file", like_this_name)
    new_name = "%s/%s"%(taxi_stand,name)
    fptr =  open(new_name, "w+")
    for line in lines:
        fptr.write(line)
    fptr.close()
    print( "wrote", new_name)

#end

