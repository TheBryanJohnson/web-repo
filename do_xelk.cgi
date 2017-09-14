#!/usr/bin/python
import cgi

print 'Content-type: text/html\n\n'

givenParams = cgi.FieldStorage()


allParams={
"origunits": ["Label":"Original Units", "Exists":False],
"convunits": ["Label":"New Units", "Exists":False],
"numunits": ["Label":"Number of Units", "Exists":False],
"convfactor": ["Label":"Conversion Factor", "Exists":False]
}

def checkExist():
	#parName = origunits, convunits, etc
	#parInfo = list which contains "Label", "Exists", etc
	for parName, parInfo in allParams.iteritems():
		#Check if the correct parameters were passed in to the cgi file
		if parName in givenParams:
			parInfo["Exists"] = True
		
def checkInput():
	 
