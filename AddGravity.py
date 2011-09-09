#! /usr/bin/env python

#Adds GravityBoundaryType to a hierarchy file
#Probably does subgrids properly, but need to double check.  

#Call from unix prompt:
# %> AddGravity.py <HierarchyName>
#
# Doesn't error check, so only run if you know gravity isn't on. (Or, write the error check)
# Saves the old hierarchy as hierarchyname.Old

# Parse of command line and call happens after definition primary (only) routine "ag"
#
# Flow:
# 1.) Open file, read all lines
# 2.) Declare empty Hierarchy
# 3.) Put each Old line in New Hierarchy.
# 4.) Flag if finished with the root grid (which always comes first.)
# 5.) Root Grids get GravityBoundaryType = 0, Subgrids get 2.  Insert the proper one after
#     the line NumberOfParticles.

def ag(filename="data0001.hierarchy"):

#	Open file and read lines, declare new (empty) hierarchy

	file = open(filename, "r")
	AllLines = file.readlines()
	NewLines = []
#	close file.  (duh.)		
	file.close()

#	Loop over lines.  For each one, query for "NumberOfParticles", because boundary type
#	needs to go after it.

#	The root grids all come first, so ThisIsASubGrid is 0 until NextGridTHisLevel = 0,
#	whence its chaged to 1.  True, there will be more than one NGTL = 0, but only
#	the first one is important for us.
	ThisIsASubGrid = 0

	for line in AllLines:

		NewLines.append(line)
#		Set Grid Number.  Not used right now, but may be necessary later.
		if line.find("Grid =") != -1:
			GridNumber = int( line[6:-1] )

#		If NextGridThisLevel == 0, then we're done with the root grid.  All others are
#		SubGrids, and should get the appropriate SubGrid flag.  (may still be buggy...)

		
		if line.find("NextGridThisLevel = 0") != -1:
			ThisIsASubGrid = 1

#		The GravityBoundaryType needs to go after NumberOfParticles.
		if line.find("NumberOfParticles") != -1:
			if ThisIsASubGrid == 0:		
				NewLines.append("GravityBoundaryType = 0\n")
			else:
				NewLines.append("GravityBoundaryType = 2\n")


#	Now that we're done with the parse, write the new hierarchy file.


	OldFileName = filename + ".OLD"
	NewFilename = filename

#	write new file
	file = open(NewFilename, "w")
	print " "
	print "writing ", NewFilename, ", saving the old as", OldFileName
	print "Also: change MaximumGravityRefinementLevel to reflect the new change in gravity."
	print " "
	for newline in NewLines:
		file.write(newline)	
	file.close()

#	write Old File
	file = open(OldFileName, "w")
	for newline in AllLines:
		file.write(newline)
	file.close()
#end

#
# Now the command line parse.
#

import sys


if len(sys.argv) == 1:
	print "Add's the Gravity Boundary to the Hierarchy File."
	print "%> AddGravity <HierarchyName>"
	print "   Returns HierarchyName with the gravity added, saves the old one as HierarchyName.OLD"
else:
	for Filename in sys.argv[1:]:
		ag(Filename)
