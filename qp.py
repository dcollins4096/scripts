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

	OutName = DirName + "/"+filename
	file = open(filename, "r")

	lines = file.readlines()

	stack = []
	output = []
	debug = 0
	Another = -1
	elifWarn = """
	WARNING:  Your desired pre-processor directive is inside an if ... elif ... construct.
		Our desire to leave the 'other' directives intact posed a problem with this 
		type of construct.  Here, all defines are assumed to be ON unless otherwise
		explicitly stated, so we have no way of knowing that there's an implied negation
		of one variable by the existance of another.

		Contact dcollins if you really need this done, we can discuss a work around.
		"""
		
#	figure out what the negation is
	Ndefine = negate(define)
	
	for line in lines:

		match = ""
		keepline = 1
		if debug == 1:
			print "---",line[0:-1]
			
		if line[0] == "#":
		 #ifdef
		 if re.findall("(#\s*ifdef\s*)([^\s]*)(.*)",line) != []:
			match = re.match("(#\s*ifdef\s*)([^\s]*)(.*)",line).group(2)
		 	stack.append(match)
		 #if defined
		 elif re.findall(r"#\s*if\s*defined\s*(.*)", line) != []:
		 	match = re.match(r"(#\s*if\s*defined\s*)\((.*)\)", line).group(2)
		 	stack.append(match)
		 #if 0
		 elif re.findall("#\s*if\s",line) !=[]:
		 	match = line[4:]
		 	stack.append(match)
		 #ifndef
		 elif re.findall("(#\s*ifndef\s*)([^\s]*)",line) != []:
			match = negate( re.match("(#\s*ifndef\s*)([^\s]*)",line).group(2) )
		 	stack.append(match)
		 #endif
		 elif re.findall("#\s*endif",line) != []:
		 	match = stack.pop()
			while (stack != [] and stack[-1] == Another):
				tmp = stack.pop()
				tmp = stack.pop()
				if tmp == define or tmp == Ndefine:
					keepline = 0
		 #else
		 elif re.findall("#\s*else",line) != []:
		 	match = stack.pop()
		 	stack.append( negate(match) )
		 #elif (doesn't quite work)
		 elif re.findall("#\s*elif",line) != []:
			if stack.count(define) !=0 or stack.count(Ndefine) !=0:
				print elifWarn
				return 0
		 	match2 = stack.pop()
		 	match = re.match(r".*(defined\s*)\((.*)\)", line).group(2)
			stack.append( negate(match2) )
			stack.append(Another)
		 	stack.append(match)
		 #Things I don't care about, but I want to cover my bases.
		 #include
		 elif re.findall("#\s*include",line) != []:
			#don't care about include values.
			match = ""
		 #define
		 elif re.findall("#\s*define",line) != []:
			#don't care about defines
			match = ""
		 #undef
		 elif re.findall("#\s*undef",line):
			match = ""

		 #shell environment.
		 elif re.findall("#!",line):
			 
		        match = ""
		 else:
		        print "Directive given by:"
			print line
			print "didn't match anything."
			print "(in order to keep us honest, I tried to ensure that all directives"
			print " were acknowledged.  This one is missing.)"
			return 0


		#if this line has anything to do with my directive,
		#i don't want it

		if match == define:
			continue
		if match == Ndefine:
			continue
		if keepline == 0:
			continue

		#the only lines I don't write are the ones I've been told not to.
		if stack.count(Ndefine):
			continue
		output.append(line)

		if debug == 1:
			print "   ***",line[0:-1]

	#
	# Now write the file!
	#


	file = open(OutName, "w")
	for line in output:
		file.write(line)
	file.close()				
	return 1
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
#  QuickPre  #define filename (or names)
#
# Output is put into the QuickPreDir directory, made in the working directory.
#
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
		if QP(define, value,name) == 0:
			print "error found in ", name
			break

	if len(sys.argv) -  filenamestart > 1:
		print """
To catch the non-pre-processed files, C&P the following:
foreach i (*)
	if( ! ( -e QuickPreDir/$i ) ) then
		cp $i QuickPreDir
	endif
end
"""
#end
