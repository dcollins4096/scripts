#! /usr/bin/env python

#this is a comment
"""
parses datastar output.
from csh:
	python <loads python>
	import moo <loads and compiles moo, saves moo.pyc>
	reload(moo) <recompiles>	
	moo.parse(bla ,bla)			
	OR
	from moo import *
	parse(bla,bla)
"""
#slightly more complicated, uses regular expressions
#Reads in Filename, parses it into lines that begin with "n:"
#Also looks at leftover, un-filed lines. (for system things, not enough proc)
def parse(FileName,NumProcs):
# regular expressions mod
	import re

#file manip
	file = open(FileName,"r")     
	lines = file.readlines()
	file.close()

	for i in range(0,NumProcs):
		print "opening ", str(i)+".err"
#open file for processor
		moo = open(str(i)+".err","w")


                #This is a hack: there are better ways to get regular expressions to do my bidding.
                if i >= 1000:
                    expr = re.compile("^"+str(i)+":")
                else:
                    expr = re.compile("\D"+str(i)+":")

		for lnum in range( 0, len(lines) ):
#		for line in lines:


			
			if lines[lnum] != "" :
				match = expr.findall( lines[lnum] )
				if len( match ) > 0:
					moo.write( lines[lnum] )
					lines[lnum] = ""
		moo.close() 
	moo = open("others.err", "w")
	for lnum in range( 0, len(lines) ):
		if lines[lnum] != "":
			moo.write(lines[lnum])
	moo.close()
	
#end that shit

#a simple minded parser
def parseOld(FileName,NumProcs):
	file = open(FileName,"r")		
	lines = file.readlines()
	for i in range(0,NumProcs-1):
		moo = open(str(i)+".err","w")
		for line in lines:
			if line.find(str(i)+":") != -1:
				moo.write(line)
		moo.close() 
	file.close()


import sys
import glob

if len(sys.argv) < 3:
	print """
	%> Parse.py filename nprocessors
	returns 0.err, etc.
	assumes lines start with
        ^  n:
	where n is the processor.
	Future versions might not need the number of processors given.
"""
else:
	filename = sys.argv[1]
	nproc = int(sys.argv[2])
	if glob.glob(filename) == []:
		print "Hey!", filename, "doesn't exist, ya jerk."
	else:
		parse(filename, nproc)

#end
