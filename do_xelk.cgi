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

def main():
	checkExist()
	checkInput()
	#for parName, parInfo in allParams.iteritems():
	#	print parName, parInfo["Exists"], parInfo["Value"], parInfo["Valid"]
		
	
main()
