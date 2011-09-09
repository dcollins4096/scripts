#!/usr/bin/env python
#
# The quick pre-processor.  Only toggles single #ifdefs. 
#
# Useful for hacking our large swaths of code for a modified  
# source code release. 
# 
# Usage: 
#  QuickPre #define filename (or names)
#
# Output is put into the QuickPreDir directory.
# For NOT defining (so it kicks off ifndefs) use "not name".
# Note: Somehow I still need to get the value input.  Probably needs a flag or something.


import sys
import os
import glob
import re
#
# QP does all the work.
#

def negate(string):
	if string[0] == "!":
		return string[1:]
	else:
		return "!"+string

#end negate
def QP(define, value, filename):
	print "===== def ", define, " filename " , filename, " ====="

	DirName = "./QuickPreDir"	

	#debug output level.  
	dbg_lev = 0

# check for file existance
# read it (or complain if it doesn't exist)
# foreach line: 
#  (future development)
#  (pull out comments, quotes)
#  (if NOT ifdef, ifndef, )
#  ( Examine line for the word, probably wants a regexp.)
#  ( if found, replace existance with value.)
#  If line begins with #ifdef, push argument onto the ifdef stack
#  If line begins with #ifndef, push !argument onto the ifdef stack
#  If line begins with #endif, pop ifdef stack.
#  if line begins with #else, pop ifdef, push !argument
#  If the ifdef stack isn't empty:	
#   If (any) define matches anything in the stack, copy line to output array
#   If (any) !define matches anything in the stack, don't copy line.
# write crap.

#	error check.
	if glob.glob(filename) == []:
		print "Missing ", filename
		return

	if filename == DirName:
		return
	
	OutName = DirName + "/"+filename
	file = open(filename, "r")

	lines = file.readlines()

	stack = []
	output = []
#	figure out what the negation is: inside Ndefine, lines aren't written.

	Ndefine = negate(define)

	for line in lines:
		if dbg_lev > 0:
			print line[0:-1]
		if dbg_lev > 1:
			print "------",stack
		match = ""

		caught_case = 0
#		if re.findall(r"^#\s*ifdef\s*",line) != []:
		if line[0:6] == "#ifdef":
			match = re.findall(r"#ifdef\s*(.*)", line)[0]
			stack.append(match)
			caught_case = 1
			if dbg_lev > 1:
				print "------ match ^#ifdef"
		if re.findall(r"#if\s*defined\s*(.*)", line) != []:
			match = re.match(r"(#if\s*defined\s*)\((.*)\)", line).group(2)
			stack.append(match)
			caught_case = 1
			if dbg_lev > 1:
				print "------ match if defined"
		if line[0:7] == "#ifndef":
			match = negate( re.findall(r"#ifndef\s*(.*)", line)[0])
			stack.append(match)
			caught_case = 1
			if dbg_lev > 1:
				print "------ match ifndef"
		if line[0:6] == "#endif":
			match = stack.pop()
			caught_case = 1
			if dbg_lev > 1:
				print "------ match endif"
		if line[0:5] == "#else":
			match = stack.pop()
			stack.append( negate(match) )
			caught_case = 1
			if dbg_lev > 1:
				print "------ match else"

		#some 'other' if statement, probably worth skiping.
		if re.findall(r"#if\s*(.*)", line) != [] and caught_case == 0:
			match = line[3:]
			stack.append(match)
			caught_case = 1
			if dbg_lev > 1:
				print "------ match something other:", line[0:-1]

		#
		# Cases that don't affect the stack, but we watch for.
		#
				
		if re.findall(r"#\s*define\b",line) != []:
			caught_case = 1

		if re.findall(r"#\s*include",line) != []:		
			caught_case = 1

		if re.findall(r"#\s*undef",line) != []:
			caught_case = 1
		if line[0:5] == "#elif":
			print "#elif encountered: ignoring.  Output code might not compile..."
			caught_case = 1
		if line[0] == "#" and caught_case == 0:
			print "You missed a cpp case:"
			print "--- ", line[0:-1]

#			match2 = stack.pop()
#			match = re.findall(r"#elif\s*defined\s*\((.*)\)",line)
#			stack.append(match)

		#print "---",line[0:-1], "(",match, ")"

		#if this line has anything to do with my directive,
		#i don't want it
		if match == define:
			continue
		if match == "!" +define:
			continue
		if match == Ndefine:
			continue

		#the only lines I don't write are the ones I've been told not to.
		if stack.count(Ndefine):
			continue
		output.append(line)
		

	#
	# Now write the file!
	#


	file = open(OutName, "w")
	for line in output:
		file.write(line)
	file.close()				
#end QP

#
# Command Line crap.
#


if len(sys.argv) == 1:
	print """
#
# The quick pre-processor.  Only toggles single #ifdefs. 
# Useful for hacking our large swaths of code for a modified  
# source code release. 
# 
# Usage: 
#  %> QuickPre.py  define filename (or names)
# i.e.
#  %> QuickPre.py MHD *
#    will look through every file in the directory, and define MHD.
#  
#  %> QuickPre.py not MHD * 
#    will parse every file with MHD undefined.  
#  Each file so parsed is placed in a directory called QuickPreDir
#  Only one define can be called at a time.
"""
else:
	# Make the output directory
	
	DirName = "./QuickPreDir"


	if glob.glob(DirName) == []:
	        os.mkdir(DirName)
	
	filenamestart = 2
	if sys.argv[1] == "not":
		define = "!" + sys.argv[2]
		filenamestart = 3
	else:
		define = sys.argv[1]
	value = 0   #not used currently.
	
	# for each argv, call 'split'
	for name in sys.argv[filenamestart:]:
		QP(define, value,name)


#end
