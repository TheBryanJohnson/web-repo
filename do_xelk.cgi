#!/usr/bin/python

#William Miller
#Bryan Johnson
#CS316 project 1 - a cgi script written in python to help an alien with some unit conversions.
#Only converts units as specified in acompanying html form, xelk.html.

import cgi

print 'Content-type: text/html\n\n'

givenParams = cgi.FieldStorage()

#Data structure to hold all information for the system
#Could initialize all values in a loop, left them here for clarity
allParams={
"origunits": {"Label":"Original Units", "Exists":False, "Value":None, "Valid":False},
"convunits": {"Label":"New Units", "Exists":False, "Value":None, "Valid":False},
"numunits": {"Label":"Number of Units", "Exists":False, "Value":None, "Valid":False},
"convfactor": {"Label":"Conversion Factor", "Exists":False, "Value":None, "Valid":False}
}

#Strings considered as valid units when passed in through the form.
#Note, system does not account for variation in capitalization or plurl forms of the units.
validUnits = ["parsec", "lightyear", "xlarn", "galacticyear", "xarnyear", "terrestrialyear", "kilometer", "terrestrialminute"]

#Tupples containing how must of unit 1 is represented by unit 2;
#eg, for first factor, 1 parsec = 3.26 lightyears
CONV_FACTORS = [
("parsec", 3.26, "lightyear"),
("lightyear", 3.086e13, "kilometer"),
("xlarn", 7.3672, "parsec"),
("galacticyear", 250000000, "terrestrialyear"),
("xarnyear", 1.2579, "terrestrialyear"),
("terrestrialyear", 525600, "terrestrialminute")
]

#Funtion to check the existence of each parameter specified by allParams
def checkExist():
	#parName = origunits, convunits, etc
	#parInfo = list which contains "Label", "Exists", etc
	for parName, parInfo in allParams.iteritems():
		#Check if the correct parameters were passed in to the cgi file
		if parName in givenParams:
			parInfo["Exists"] = True
			#Map param values into data structure
			parInfo["Value"] = givenParams[parName].value
		
#Function to check the validity of each parameter specified by allParams
def checkInput():
	#numunits and convfactor must be some type of numerical objects
	numunits = allParams["numunits"]["Value"]
	convfactor = allParams["convfactor"]["Value"]
	#The objects are coming through as 'NoneType'; try to cast them into floats
	#with some generic error handling
	try:
		allParams["numunits"]["Value"] = float(numunits)
		allParams["numunits"]["Valid"] = True
	except:
		pass
	try:
		allParams["convfactor"]["Value"] = float(convfactor)
		allParams["convfactor"]["Valid"] = True
	except:
		pass
	
	#origunits and convunits must both exist in validUnits
	#Since there's only two checks, did not bother looping
	if allParams["origunits"]["Value"] in validUnits:
		allParams["origunits"]["Valid"] = True
	if allParams["convunits"]["Value"] in validUnits:
		allParams["convunits"]["Valid"] = True

#Converts unit1 to unit2 using the tupples in CONV_FACTORS
#unit1: string, first unit in conversion
#unit2: string, second unit in conversion
#Returns the converted answer if all parameters are correct.
#If not, returns None.
def convUnits(unit1, unit2):
	amt = allParams["numunits"]["Value"]
	for tup in CONV_FACTORS:
		if unit1 == tup[0] and unit2 == tup[2]:
			return amt*tup[1]
		if unit1 == tup[2] and unit2 == tup[0]:
			return amt/tup[1]
	return None

#Parses the HTML into a webpage to display the answers and/or errors for a particular execution of the script.
#Returns HTML as a large string.
def parseHTML():
	#If there's any invalidity found in the parameters, this becomes True
	invalidInput = False
	
	#Template for the top of the rendered HTML doc
	top = """
	<head>
  	<title>Galactic Conversion</title>
	</head>
	<body style="background-color: #ffff99;">
  	"""

	#Template for the bottom of the rendered HTML doc
	bottom = """
	</body>
	</html>
	"""

	parms = [allParams["origunits"], allParams["convunits"], allParams["numunits"], allParams["convfactor"]]

	#Essentially, based on the flags put up earlier in the program, append one of two <h3> tags with appropriate text
	#for each parameter
	for param in parms:	
		if param["Exists"] and param["Valid"]:
			top += "<h3 style='color:blue;'>"+str(param["Label"])+": \""+str(param["Value"])+"\"</h3>"
		else:
			top += "<h3 style='color:red;'>"+str(param["Label"])+": Parameter missing or bad!</h3>"
			invalidInput = True

	#Append one final <h3> tag with one of three messages; 
	#1) Error message if parameters are bad or missing
	#2) Answer to the conversion if all parameters are valid
	#3) Error message if valid units are entered, but the combination is not valid (eg, parsec to kilometer)
	if invalidInput:
		top += "<h3 style='color:red;'>Invalid input! Make sure all parameters are present and correct.</h3>"
	else:
		conv = convUnits(allParams["origunits"]["Value"], allParams["convunits"]["Value"])
		convFact = allParams["convfactor"]["Value"]
		#if conv is actually a valid conversion
		if conv is not None:
			top += "<h3 style='color:green;'>Answer: "+str(conv*convFact)+"</h3>"
		else:
			top += "<h3 style='color:red;'>Invalid conversion between parameters; see conversion chart for valid combinations</h3>"
	return top+bottom
 
		
#main function
def main():
	checkExist()
	checkInput()
	print parseHTML()

main()

#A word on the use of globals vs. function parameters:
#Probably not the best practice, but for a self-contained script, functional.
#Regardless of practice, the system's still dynamic based on the global data structures, functions
#just can't be taken out of context. Not so much a conscious design choice as it happened and
#we rolled with it. Modifying the functions to take parameters wouldn't be hard if needed.
