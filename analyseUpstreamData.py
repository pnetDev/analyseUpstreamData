#!/usr/bin/python
from __future__ import division
import sys
import statistics
#Variables
allowedDelta = 50
emptyList=0
## Current Levels
cmts=sys.argv[1]
historyFile=sys.argv[2]
MAC=historyFile.split('.')[0]

# file to open
historyFile = "/opt/analyseUpstreamData/" + str(cmts) + "/" + str(historyFile)
#print historyFile
listUSL = []

# Iterate through the history file
for modemdata in open(historyFile,'r'):
	modemdata=modemdata.replace('\n', '')
	#print modemdata
	## Parse the data and append to listUSL
	usFreq = modemdata.split(',')[3]
	usl =   modemdata.split(',')[6]
	## Check for invalid data
	if not usFreq:
		continue
	if not usl:
		continue
	usl = int(usl)
	usl = usl/10
	listUSL.append(usl)
	#print str(MAC) + " Calculating standard deviation"


print "listUSL",historyFile,listUSL
if not listUSL:
	emptyList = True
if emptyList <> True:
	uslMean = statistics.mean(listUSL)
	uslStDev = statistics.stdev(listUSL)
	#uslMode = statistics.mode(listUSL) ## Getting  equally common values errors
	usl_max_value = max(listUSL)
	usl_min_value = min(listUSL)
	#print str(MAC) + ",stdDeviation," + str(uslStDev)

	print cmts,MAC,uslStDev,usl_max_value, usl_min_value, uslMean
	if uslStDev > 3:
		print "stDevFail",cmts,MAC,uslStDev,usl_max_value, usl_min_value, uslMean
