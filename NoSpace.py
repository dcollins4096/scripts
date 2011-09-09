#! /usr/bin/env python

#
# Replaces spaces in strings with _
# 

def NoSpace(string):
	out = ""
	for char in string:
		if char == " ":
			out = out + "_"
		else:
			out = out + char
	return out



import sys

if len( sys.argv ) == 1:
	print "strig_without_spaces = NoSpace('string with spaces')"
else:
	for string in sys.argv[1:]:
		print NoSpace( string )

#end