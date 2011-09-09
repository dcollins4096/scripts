#!/usr/bin/env python

import sys
import re

def changer(filename,NewGhostZones = 5):

    infile = open(filename,"r")
    outfile = open(filename+".new","w")



    lines = infile.readlines()

    dim_re = re.compile("GridDimension\ *=\ +(\d+)\ +(\d+)\ +(\d+)")
    start_re = re.compile("GridStartIndex\ *=\ +(\d+)\ +(\d+)\ +(\d+)")
    end_re = re.compile("GridEndIndex\ *=\ +(\d+)\ +(\d+)\ +(\d+)")
    OldGhostZones = -1
    for line  in lines:
        match = start_re.match(line)
        if match != None:
            nx = int(match.group(1))
            ny = int(match.group(2))
            nz = int(match.group(3))
            if nx != ny or ny != nz:
                print "Ghost zone problem: Start Index = ",nx,ny,nz
                return
            else:
                OldGhostZones = nx
            break

    if OldGhostZones == -1:
        print "Error finding old ghost zones"
        return
    
    Difference = OldGhostZones - NewGhostZones
    
    for line in lines:

        match = dim_re.match(line)
        if match != None:
            nx = int( match.group(1) ) - 2 * Difference
            ny = int( match.group(2) ) - 2 * Difference
            nz = int( match.group(3) ) - 2 * Difference
            outfile.write("GridDimension  = %d %d %d\n"%(nx,ny,nz))
            continue
        match = start_re.match(line)
        if match != None:
            nx = int( match.group(1) ) - Difference
            ny = int( match.group(2) ) - Difference
            nz = int( match.group(3) ) - Difference
            outfile.write("GridStartIndex  = %d %d %d\n"%(nx,ny,nz))
            continue
        match = end_re.match(line)
        if match != None:
            nx = int( match.group(1) ) - Difference
            ny = int( match.group(2) ) - Difference
            nz = int( match.group(3) ) - Difference
            outfile.write("GridEndIndex  = %d %d %d\n"%(nx,ny,nz))
            continue
        outfile.write(line)
    infile.close()
    outfile.close()
    
              
if len(sys.argv) != 3:
    print "GhostZoneChanger.py <hierarchy file> <new number of ghost zones>"
    print "changes the number of ghost zones in <hierarchy file> to <new number>"

else:
    filename = sys.argv[1]
    number = int(sys.argv[2])
    changer(filename,number)
#end
