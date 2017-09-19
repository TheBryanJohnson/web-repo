#!/usr/bin/python
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

validUnits = ["parsec", "lightyear", "xlarn", "galacticyear", "xarnyear", "terrestrialyear", "kilometer", "terrestrialminutes"]

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
	#numunits and convfactor must be a float or int
	numunits = allParams["numunits"]["Value"]
	convfactor = allParams["convfactor"]["Value"]
	#Could have made this a loop, didn't since it's only 2 checks and would invole
	#chopping up the data structure
	if isinstance(numunits, (int, float, long)):
		allParams["numunits"]["Valid"] = True
	if isinstance(convfactor, (int, float, long)):
		allParams["convfactor"]["Valid"] = True
	
	#origunits and convunits must both exist in validUnits
	#Same as above, did not bother looping
	if allParams["origunits"]["Value"] in validUnits:
		allParams["origunits"]["Valid"] = True
	if allParams["convunits"]["Value"] in validUnits:
		allParams["convunits"]["Valid"] = True

def main():
	checkExist()
	checkInput()
	for parName, parInfo in allParams.iteritems():
		print parName, parInfo["Exists"], type(parInfo["Value"]), parInfo["Valid"]
	
main()
