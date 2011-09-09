#! /usr/bin/env python

#Parses the Hierarchy file and writes a geomview file that IDL can read.
#Why that idl can read?  'Cause I have an IDL script that writes GEOMview file already.
#Could I make this write the geomview directly? Maybe.  Look into that in the future.
#
#
#This is command line executable.  Usage:
# % > GVH.py <HierarchyFileName>
# Returns HierarchyFileName.Geom
# Accepts lists.
# This file contins three routines used for processing the hierarchy file.  They are:
#
# (moved to PythonStuff.py)
# IsNum(char)
# 	Accepts a character, returns 0 if it's not a numeric (or decimal ) character, 1 if it is.
#	Used in gn(), described below.
# gn(string)
#	Accepts a string and returns a list of the number is said string.  For insance,
# 	gn("a3bbb3 99.1") returns [3,3,99.1].  Called by gv(), described below.
# gv(HierarchyFileName)
# 	Accepts a hierarchy file name, and writes HierarchyFileName.Geom.  Main calling procedure, does all the work.
#	
# At the bottom of this script you'll find the wrapper that parses the command line arguments.
#
# dcc 12/30/05
#

from PyTools import *

#
# gv(filename)
#

def gv(filename="data0001.hierarchy"):

	OutFileName = filename + ".Geom"

#	Open file and read lines, declare new (empty) hierarchy

	file = open(filename, "r")
	AllLines = file.readlines()

	Lefts = []
	Rights = []
	Widths = []
	Starts = []
	Ends = []
#	close file.  (duh.)		
	file.close()

#	Loop over lines.  For each one, query for "NumberOfParticles", because boundary type
#	needs to go after it.

#	The root grids all come first, so ThisIsASubGrid is 0 until NextGridTHisLevel = 0,
#	whence its chaged to 1.  True, there will be more than one NGTL = 0, but only
#	the first one is important for us.
	ThisIsASubGrid = 0

	for line in AllLines:
#	for i in range(0,23):

#		THis is a kludge, for authoring.
#		line = AllLines[i]
#		print line[0:-1]


#		Set Grid Number.  Not used right now, but may be necessary later.
		if line.find("Grid =") != -1:
			GridNumber = gn(line)

#		Set GridRank.  
		if line.find("GridRank") != -1:
			GridRank = gn(line)

#		get StartIndex, EndIndex, LeftEdge, Right Edge.
			
		if line.find("GridStartIndex") != -1:
			Starts.append(gn(line))
#			print "     " , Starts
		if line.find("GridEndIndex") != -1:
			Ends.append(gn(line))
#			print "     " , Ends
		if line.find("GridLeftEdge") != -1:
			Lefts.append(gn(line))
#			print "     " , Lefts
		if line.find("GridRightEdge") != -1:
			Rights.append(gn(line))
#			print "     " , Rights
#		If there are more Rights than Widths, calculate new widths.	
		if len( Rights ) > len( Widths ):
#			print "     rrr0" , Rights	

#			Fun python fact: this used to be Widths.append(Rights[-1])
#			But that made Widths[-1] a POINTER to Rights[-1]
#			my love for python decreased with the following loop

			Widths.append([])
			for dim in range(0,GridRank):
				Widths[-1].append(0.0)
				Widths[-1][dim] += Rights[-1][dim]
				Widths[-1][dim] -= Lefts[-1][dim]
				Widths[-1][dim] /= (Ends[-1][dim]-Starts[-1][dim]+1)



	file = open(OutFileName,"w")
	GridRank = len( Rights[-1] )
	file.write(str(len(Rights))+"\n")

	for i in range(0,len(Rights)):
		for dim in range(0,GridRank):
			file.write(str(Lefts[i][dim])+ " ")
		file.write("\n")
		for dim in range(0,GridRank):
			file.write(str(Rights[i][dim])+ " ")
		file.write("\n")
		for dim in range(0,GridRank):
			file.write(str(Widths[i][dim])+ " ")
		file.write("\n")

	file.close()
#end


#
# Here's the command line parse and general wrapper.
#

import sys
import glob

filenames = []
if len(sys.argv) == 1:
	filenames = glob.glob("*.hierarchy")
else:
	if sys.argv[1] == "-help":
		print """
   
   Parses the Hierarchy file and writes a geomview file that IDL can read.
   IDL kind of sucks at string parsing, and pythong sucks at making images.
   This is command line executable.  Usage:
    % > GVH.py <HierarchyFileName>
    Returns HierarchyFileName.Geom
"""
	else:
		filenames = sys.argv[1:]		
		print '"gvy.py -help" for help'
for filename in filenames:
	#The string addition of filename + ", will write" is to skirt the automatic space python adds
	print "Parsing", filename+ ", will write", filename+".Geom"
	gv(filename)

#that all, folks.