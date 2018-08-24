#!/usr/bin/python

## CM 21/06/18 Just focussing on upstream errors.
## CM 21/05/18 This script polls a CMTS and returns the levels and US error counters of online modems. It repeats and logs any modems which have incrementing US errors.
## The user supplies the CMTS name and upstream interface index.

## usage pollAllOnlineModemsListIndexLogFails.py mish1 9


## Writing the online IPs to a file instead of a list
## CM Added code which checks that the correct modem is being compared. Returns an error if the MACs don't match. 

from __future__ import division
from time import gmtime, strftime
import sys,time,subprocess
from easysnmp import snmp_get, snmp_set, snmp_walk

# Variables:
now = strftime("%y%m%d%H")
## Levels Oids
currDate = str(now)

logFile = '/var/log/pollModemCounters.Log'
cmts = sys.argv[1]
usIF = sys.argv[2]

firstStats = []
secondStats = []

mac=".1.3.6.1.2.1.2.2.1.6.2"
dfq=".1.3.6.1.2.1.10.127.1.1.1.1.2.3"
ufq=".1.3.6.1.2.1.10.127.1.1.2.1.2.4"
dsp=".1.3.6.1.2.1.10.127.1.1.1.1.6.3"
snr=".1.3.6.1.2.1.10.127.1.1.4.1.5.3"
txp=".1.3.6.1.2.1.10.127.1.2.2.1.3.2"
unr=".1.3.6.1.2.1.10.127.1.1.4.1.2.3"
cor=".1.3.6.1.2.1.10.127.1.1.4.1.3.3"
unc=".1.3.6.1.2.1.10.127.1.1.4.1.4.3"

## Bonded Channel Oids
dfq2=".1.3.6.1.2.1.10.127.1.1.1.1.2.48"
dsp2=".1.3.6.1.2.1.10.127.1.1.1.1.6.48"
snr2=".1.3.6.1.2.1.10.127.1.1.4.1.5.48"
unr2=".1.3.6.1.2.1.10.127.1.1.4.1.2.48"
cor2=".1.3.6.1.2.1.10.127.1.1.4.1.3.48"
unc2=".1.3.6.1.2.1.10.127.1.1.4.1.4.48"

#Functions
def getOid(oid):
	try:
        	snmpData = snmp_get(oid, hostname=cmIP, community='private', version=2)
        	return snmpData.value
	except:
		return "1000" ## If there is a data read error

def mac2decimal(mac):
	mac = mac.split(':')
	## Need to convert each hextet to decimal and then build the dotted decimal result. Might be a better way to do this, can't find a function.
        ## Break up the MAC address into hextets H stands for Hextet
        macH0 = mac[0]
        macH1 = mac[1]
        macH2 = mac[2]
        macH3 = mac[3]
        macH4 = mac[4]
        macH5 = mac[5]
	## Convert each hextet to decimal
        dec0 = int(macH0, 16)
        dec1 = int(macH1, 16)
        dec2 = int(macH2, 16)
        dec3 = int(macH3, 16)
        dec4 = int(macH4, 16)
        dec5 = int(macH5, 16)
	macDottedDecimal = "." + str(dec0) + "." + str(dec1) + "." + str(dec2) + "." + str(dec3) + "." + str(dec4) + "." + str(dec5)
	return macDottedDecimal

def getCmIndex(macDottedDecimal,cmts):
	cmIndex = ".1.3.6.1.2.1.10.127.1.3.7.1.2" + macDottedDecimal
        cmIndexData = snmp_get(cmIndex,hostname=cmts, community='private', version=2)
        cmIndexData = cmIndexData.value
	return cmIndexData	

def getUpstreamErrors(cmts,cmIndex):
        cmUsErrors = ".1.3.6.1.2.1.10.127.1.3.3.1.12." + str(cmIndex)
        cmUsErrorsData = snmp_get(cmUsErrors,hostname=cmts, community='private', version=2)
	return cmUsErrorsData.value
	
def getCmIfIndex(cmts,cmIndex):
	getCmIfIndex = ".1.3.6.1.2.1.10.127.1.3.3.1.5." + str(cmIndex)
	getCmIfIndexData  = snmp_get(getCmIfIndex,hostname=cmts, community='private', version=2)
	return getCmIfIndexData.value

## MAIN
print "Script still under development"
print "-------------------------------------------------------------------------------"
print "Generating list of online modems on" , cmts, "upstream interface", usIF,"please wait....."
print "-------------------------------------------------------------------------------"
subprocess.check_output(['bash','get_cmtsstatustable.sh',cmts,usIF])
#modems=modems.split(',')
#print "DEBUG: Modem List",modems

print "First Check"
for cmIP in open("modems",'r'):
	cmIP = cmIP.replace("\n","")
	#print "processing", cmIP
	try:
		mac = snmp_get('.1.3.6.1.2.1.2.2.1.6.2.', hostname=cmIP, community='private', version=2)
		mac = ':'.join('{:02x}'.format(ord(x)) for x in mac.value)  ## This nifty code presents the MAC in readable format
	except:
		 print "MAC Unable to contact", cmIP, "setting MAC to 00:00:00:00:00"
                 mac = "00:00:00:00:00:00"
	macDecimal = mac2decimal(mac)
        cmIndex = getCmIndex(macDecimal,cmts)
	cmIfIndex = getCmIfIndex(cmts,cmIndex)
	## Skip if its not the index the user entered
	if cmIfIndex <> usIF:
		continue ## Skip this iteration
        UsErrors = getUpstreamErrors(cmts,cmIndex)
	dsFreq = getOid(dfq)
	usFreq = getOid(ufq)
	DSP = getOid(dsp)
	SNR = getOid(snr)
	TXP = getOid(txp)
	UNR = getOid(unr)
	COR = getOid(cor)
	UNC = getOid(unc)
	dsFreq2 = getOid(dfq2)
	DSP2 = getOid(dsp2)
	SNR2 = getOid(snr2)
	UNR2 = getOid(unr2)
	COR2 = getOid(cor2)
	UNC2 = getOid(unc2)
	macDecimal = mac2decimal(mac)
	cmIndex = getCmIndex(macDecimal,cmts)
	UsErrors = getUpstreamErrors(cmts,cmIndex)
	cmIfIndex = getCmIfIndex(cmts,cmIndex)
	#print mac, cmIP, "DSFREQ:", dsFreq, "USFREQ:", usFreq, "PWR:", DSP, "SNR:", SNR, "TX PWR:", TXP, "Packets:",UNR, "Corrected:", COR, "Down Uncorrected:", UNC, "Up Uncorrected:", UsErrors

	## Check are we dealing with a bonded modem
	#if dsFreq2 <> "NOSUCHINSTANCE":
	#	print "1st Check",cmts,mac,cmIP,dsFreq,usFreq,DSP,SNR,TXP,UNR,COR,UNC,UsErrors,"ifIndex:",cmIfIndex, "Bonded Stats",dsFreq2,DSP2,SNR2,COR2,UNC2
	#	firstStats.append([cmts,mac,cmIP,dsFreq,usFreq,DSP,SNR,TXP,UNR,COR,UNC,UsErrors,cmIfIndex,dsFreq2,DSP2,SNR2,COR2,UNC2])
	firstStats.append([cmts,mac,cmIP,dsFreq,usFreq,DSP,SNR,TXP,UNR,COR,UNC,UsErrors,cmIfIndex])
	print "1st Check",cmts,mac,cmIP,dsFreq,usFreq,DSP,SNR,TXP,UNR,COR,UNC,UsErrors,"ifIndex:",cmIfIndex

#print firstStats
print ""

#for data in firstStats:
#	print data[0], data[1]
#print ("\n".join(firstStats))
print "\n"

print "Second Check"
for cmIP in open("modems",'r'):
	cmIP = cmIP.replace("\n","")
        #print "processing", cmIP
        try:
                mac = snmp_get('.1.3.6.1.2.1.2.2.1.6.2.', hostname=cmIP, community='private', version=2)
                mac = ':'.join('{:02x}'.format(ord(x)) for x in mac.value)  ## This nifty code presents the MAC in readable format
        except:
                print "MAC Unable to contact", cmIP, "setting MAC to 00:00:00:00:00:00"
                mac = "00:00:00:00:00:00" 
	macDecimal = mac2decimal(mac)
        cmIndex = getCmIndex(macDecimal,cmts)
        cmIfIndex = getCmIfIndex(cmts,cmIndex)
        ## Skip if its not the index the user entered
        if cmIfIndex <> usIF:
                continue ## Skip this iteration
        dsFreq = getOid(dfq)
        usFreq = getOid(ufq)
        DSP = getOid(dsp)
        SNR = getOid(snr)
        TXP = getOid(txp)
        UNR = getOid(unr)
        COR = getOid(cor)
	UNC = getOid(unc)
	dsFreq2 = getOid(dfq2)
        DSP2 = getOid(dsp2)
        SNR2 = getOid(snr2)
        UNR2 = getOid(unr2)
        COR2 = getOid(cor2)
        UNC2 = getOid(unc2)

        UsErrors = getUpstreamErrors(cmts,cmIndex)
	#print mac, cmIP, "DSFREQ:", dsFreq, "USFREQ:":, usFreq, "PWR:", DSP, "SNR:", SNR, "TX PWR:", TXP, "Packets:",UNR, "Corrected:", COR, "Down Uncorrected:", UNC, "Up Uncorrected:", UsErrors

	## Check are we dealing with a bonded modem
        #if dsFreq2 <> "NOSUCHINSTANCE":
        #        print "2nd Check",cmts,mac,cmIP,dsFreq,usFreq,DSP,SNR,TXP,UNR,COR,UNC,UsErrors,"ifIndex:",cmIfIndex, "Bonded Stats",dsFreq2,DSP2,SNR2,COR2,UNC2
        #        firstStats.append([cmts,mac,cmIP,dsFreq,usFreq,DSP,SNR,TXP,UNR,COR,UNC,UsErrors,cmIfIndex,dsFreq2,DSP2,SNR2,COR2,UNC2])
        
	print "2nd Check",cmts,mac,cmIP,dsFreq,usFreq,DSP,SNR,TXP,UNR,COR,UNC,UsErrors,"ifIndex",cmIfIndex
        secondStats.append([cmts,mac,cmIP,dsFreq,usFreq,DSP,SNR,TXP,UNR,COR,UNC,UsErrors,cmIfIndex])


print ""
for data in secondStats:
        print data[0], data[1]

modemCount = len(secondStats)
#print firstStats
print "-------------------------------------------------------------------------------------------"
#print secondStats

print "********* REPORT ***********"
print ""
## Calculate results
## Header cmts,mac,cmIP,dsFreq,usFreq,DSP,SNR,TXP,UNR,COR,UNC,UsErrors
## Dummy values for bonded variabled.
dsFreq1b = "NULL"

for data in range(modemCount):
	cmts1 = firstStats[data][0] 
	mac1 = firstStats[data][1] 
	cmIP1 = firstStats[data][2] 
	dsFreq1 = firstStats[data][3] 
	usFreq1 = firstStats[data][4] 
	DSP1 = firstStats[data][5] 
	SNR1 = firstStats[data][6] 
	TXP1 = firstStats[data][7] 
	UNR1 = firstStats[data][8] 
	COR1 = firstStats[data][9] 
	UNC1 = firstStats[data][10] 
	UsErrors1 = firstStats[data][11] 
	cmIfIndex1 = firstStats[data][12]
 	## Check is it a bonded modem
	"""
	try:
		dsFreq1b = firstStats[data][13] ## If the string is empty its not a bonded modem and we continue the loop
		print mac1, "is bonded"	
		dsFreq1b = firstStats[data][13]
		DSP1b = firstStats[data][14] 
		SNR1b = firstStats[data][15]
		UNR1b = firstStats[data][16]
		COR1b = firstStats[data][17]
		UNC1b = firstStats[data][18]
	except IndexError as error:
		x = 1 
		#print mac1, "not a bonded modem,"
	"""
	
	cmts2 = secondStats[data][0]
        mac2 = secondStats[data][1]
        cmIP2 = secondStats[data][2]
        dsFreq2 = secondStats[data][3]
        usFreq2 = secondStats[data][4]
        DSP2 = secondStats[data][5]
        SNR2 = secondStats[data][6]
        TXP2 = secondStats[data][7]
        UNR2 = secondStats[data][8]
        COR2 = secondStats[data][9]
        UNC2 = secondStats[data][10]
        UsErrors2 = secondStats[data][11]
	
	#cmIfIndex2 = secondStats[data][12]
	#dsFreq1b = firstStats[data][13]                                 ## Bonded
        #DSP2b = firstStats[data][14]
        #SNR2b = firstStats[data][15]
        #UNR2b = firstStats[data][16]
        #COR2b = firstStats[data][17]
        #UNC2b = firstStats[data][18]

	
	## Check that we are looking at the right comparison data.
	if mac1 <> mac2:
		print "MAC mismatch", mac1, mac2 
		print "Quiting, need to debug"	
		quit ()

	# Sanity print
	#print  cmts1,mac1,cmIP1,dsFreq1,usFreq1,DSP1,SNR1,TXP1,UNR1,COR1,UNC1,UsErrors1 + "\t" +  cmts2,mac2,cmIP2,dsFreq2,usFreq2,DSP2,SNR2,TXP2,UNR2,COR2,UNC2,UsErrors2
		
	# Calculate DS errors
	goodWordsDelta = int(UNR2) - int(UNR1)
	downHecWordsDelta = int(UNC2) - int(UNC1)
	#print "\tDEBUG: Division Calc is", downHecWordsDelta, "/", goodWordsDelta
	## If the results are zero don't do the calculation or will have division by zero problem
	if downHecWordsDelta > 0  or goodWordsDelta > 0:
		downHecPercent = (downHecWordsDelta / goodWordsDelta) * 100
		downHecPercent = round(downHecPercent,4)
	else:
		downHecPercent = 0
	
	# Calculate US errors delta
	upHecWordsDelta = int(UsErrors2) - int(UsErrors1)
	## Hard coded here
	#upHecWordsDelta = 2

	#print cmts1,mac1,cmIP1,dsFreq1,usFreq1,DSP1,SNR1,TXP1,UNR1,COR1,UNC1,UsErrors1,DSP2,SNR2,TXP2,UNR2,COR2,UNC2,UsErrors2,"goodWordsDelta:", goodWordsDelta, "downHecWordsDelta:" , downHecWordsDelta, "downHecPercent:", downHecPercent, "upHecWordsDelta:", upHecWordsDelta,"IfIndex:",cmIfIndex1
	 
	#print  cmts1,mac1,mac2,cmIP1,dsFreq1,usFreq1,DSP1,SNR1,TXP1,UNR1,COR1,UNC1,UsErrors1 + "\t" +  mac2,dsFreq2,DSP2,SNR2,TXP2,UNR2,COR2,UNC2,UsErrors2

	## Logging failures routine.
	## Is the hec% significant?
	#if downHecPercent > 0.1:
		#print "DS ERRORS:",cmts1,mac1,mac2,cmIP1,dsFreq1,usFreq1,DSP1,SNR1,TXP1,UNR1,COR1,UNC1,UsErrors1,DSP2,SNR2,TXP2,UNR2,COR2,UNC2,UsErrors2,"goodWordsDelta:", goodWordsDelta, "downHecWordsDelta:" , downHecWordsDelta, "downHecPercent:", downHecPercent, "upHecWordsDelta:", upHecWordsDelta,"IfIndex:",cmIfIndex1
	if upHecWordsDelta > 1:
		print "US ERRORS:",now,cmts1,mac1,mac2,cmIP1,dsFreq1,usFreq1,DSP1,SNR1,TXP1,UNR1,COR1,UNC1,UsErrors1,DSP2,SNR2,TXP2,UNR2,COR2,UNC2,UsErrors2,"goodWordsDelta:", goodWordsDelta, "downHecWordsDelta:" , downHecWordsDelta, "downHecPercent:", downHecPercent, "upHecWordsDelta:", upHecWordsDelta,"IfIndex:",cmIfIndex1
