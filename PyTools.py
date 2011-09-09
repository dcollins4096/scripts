
#
# Useful pythong tools.
#
# IsNum(char) returns tru or false if char is a number.
#    Might have been easily done with regular expressions, but I didn't
#    know about them when this was written
# gn(string)
#	get number.  Returns an array of the numbers in a string.
#	So gn("0 3 5") = [0,3,5]


#Is This Character numeric?  Compare against 0-9 and '.', return 0 if it isnt/
#Takes a string type object or an int type object.
def IsNum(char):

	#the flag that will be returned.
	ItIs = 0

	#the things to match
	OKthings = ['0','1','2','3','4','5','6','7','8','9','.','-', '+']
	OKthingsI= range(0,10)

	for i in OKthings:
		if char == i :
			ItIs = 1
	for i in OKthingsI:
		if char == i :
			ItIs = 1


	return ItIs

#end IsNum

#parse string into numbers
def gn(stringIn):
	"""Convert stringIn to a number or array of numbers.
	Now that I now more pythong, this is pretty ugly.  However, it's already written."""
#	NUM is a boolean, denoting a contiguous number.  
#	FLOAT is a boolean, denoting the number is a float.  (has a '.' in it)
#	TempString gets filled with the string

	NUM = 0
	FLOAT = 0
	TempString = ""
	OutArray=[]

#	The last number needs a character after it, or the next loop won't write out
#	the last number.  So addone.
	string = stringIn + " " 
	print "//"+string+"\\"
	if string == " . ":
		return [string]

	for char in string:
#	One of three things is going on:  
#		1.)this point in the string is in a number.  Save it to TempString
#		1.5) This point is a.) in a number and b.) is 'e', signifying scientific notation
#		2.)This point in the string is the end (first character after) a number.  
#			Stop, cast the temp string to a number, cat it to the OutArray
#		3.) This is not a number and not the end of a number.  Who cares, move on.

#		1.)
		if IsNum(char) == 1:
			NUM = 1
			TempString = TempString + char
			if char == ".":
				FLOAT = 1
#		2.)
#		If we just finished an integer, bung it into the output array		
		if IsNum(char) == 0 and NUM == 1:
			if char == "e":
				TempString = TempString + char
				FLOAT = 1
			else:
				NUM = 0
				if FLOAT == 1:
					OutArray.append(float(TempString))
				else:
					OutArray.append( int(TempString) )
				TempString = ""
				FLOAT = 0

#		3.) (not very exciting.)

#	one dimensional arrays are stupid.
	if len(OutArray) == 1:
		OutArray = OutArray[0]
	return OutArray

