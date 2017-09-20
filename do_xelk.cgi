#!/usr/bin/python

#William Miller
#Bryan Johnson
#CS316 project 1

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

#Possibly add support for plurl forms of units TODO 
#(would also involve changing CONV_FACTORS)
#(todo, See docs for clarification?)
validUnits = ["parsec", "lightyear", "xlarn", "galacticyear", "xarnyear", "terrestrialyear", "kilometer", "terrestrialminute"]

CONV_FACTORS = [
("parsec", 3.26, "lightyear"),
("lightyear", 3.086e13, "kilometer"),
("xlarn", 7.3672, "parsec"),
("galacticyear", 250000000, "terrestrialyear"),
("xarnyear", 1.2579, "terrestrialyear"),
("terrestrialyear", 525600, "terrestrialminute")
]


def checkExist():
	#parName = origunits, convunits, etc
	#parInfo = list which contains "Label", "Exists", etc
	for parName, parInfo in allParams.iteritems():
		#Check if the correct parameters were passed in to the cgi file
		if parName in givenParams:
			parInfo["Exists"] = True
			#Map param values into data structure
			parInfo["Value"] = givenParams[parName].value
		
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

#unit1: string, first unit in conversion
#unit2: string, second unit in conversion
def convUnits(unit1, unit2):
	amt = allParams["numunits"]["Value"]
	for tup in CONV_FACTORS:
		if unit1 == tup[0] and unit2 == tup[2]:
			return amt*tup[1]
		if unit1 == tup[2] and unit2 == tup[0]:
			return amt/tup[1]
	return None

def parseHTML():
	invalidInput = False
	

	top = """
	<head>
  	<title>Galactic Conversion</title>
	</head>
	<body>
  	"""

	bottom = """
	</body>
	</html>
	"""

	parms = [allParams["origunits"], allParams["convunits"], allParams["numunits"], allParams["convfactor"]]

	for param in parms:	
		if param["Exists"] and param["Valid"]:
			top += "<h3 style='color:blue;'>"+str(param["Label"])+": \""+str(param["Value"])+"\"</h3>"
		else:
			top += "<h3 style='color:red;'>"+str(param["Label"])+": Parameter missing or bad!</h3>"
			invalidInput = True

	if invalidInput:
		top += "<h3 style='color:red;'>Invalid input! Make sure all parameters are present and correct.</h3>"
	else:
		conv = convUnits(allParams["origunits"]["Value"], allParams["convunits"]["Value"])
		convFact = allParams["convfactor"]["Value"]
		#if conv is actually a valid conversion
		if conv is not None:
			top += "<h3 style='color:blue;'>Answer: "+str(conv*convFact)+"</h3>"
		else:
			top += "<h3 style='color:red;'>Invalid conversion between parameters; see conversion chart for valid combinations</h3>"
	return top+bottom
 
		

def main():
	checkExist()
	checkInput()
	print parseHTML()

main()
