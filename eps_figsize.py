#!/usr/bin/env python
import sys
max_x, max_y=0,0
dirname = sys.argv[1]
for filename in sys.argv[2:]:
    fptr = open("%s/%s"%(dirname,filename))
    for line in fptr:
        if line.startswith('%%BoundingBox:'):
            #print line
            nums = line.split(" ")[1:]
            x0,y0=int(nums[0]),int(nums[1])
            x1,y1=int(nums[2]),int(nums[3])
            max_x = max(max_x, x1-x0)
            max_y = max(max_y, y1-y0)
            fptr.close()
            break
#print max_x, max_y
margin = 18
paperwidth = max_x + margin
paperheight = max_y + 4*margin
optr = file('view_eps_variables','w')
optr.write("set margin = %s;\n"%(margin)) #hard coded, sorry.
optr.write("set figurewidth = %s;\n"%max_x)
optr.write("set figureheight = %s;\n"%max_y)
optr.write("set paperwidth = %s;\n"%paperwidth)
optr.write("set paperheight = %s;\n"%paperheight)
optr.write("set paperwidthInches = %s;\n"%(paperwidth/72.))
optr.write("set paperheightInches = %s;\n"%(paperheight/72.))
optr.close()


#end
