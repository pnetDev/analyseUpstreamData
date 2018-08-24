#!/bin/bash

echo ""
echo ""
source /root/.bashrc
processDir=/root/upstreamAnalysis
# 180823 CM Trying to analyse upstream data for a CM. Here is how it will work.
# Enter modemdata directory
# Read first MAC of newest file
# Generate history file of this MAC
# Python script will analyse the data
# History file is removed

# Variables
currDate=$(date +%y%m%d%H%M)
modemdata=/opt/com21/nmaps/snmp/modemdata
copy=0
# Doing a test with knock
workingDir=/opt/analyseUpstreamData
cmts=$1
echo $cmts
## Fmtn is Forth so we have to change this
if [ "$cmts" == "Fmtn1" ] ; then cmts="Forth1" ; fi
if [ "$cmts" == "Fmtn2" ] ; then cmts="Forth2" ; fi
if [ "$cmts" == "Fmtn3" ] ; then cmts="Forth3" ; fi
if [ "$cmts" == "Fmtn4" ] ; then cmts="Forth4" ; fi
if [ "$cmts" == "Fmtn5" ] ; then cmts="Forth5" ; fi
if [ "$cmts" == "Fmtn4" ] ; then cmts="Forth6" ; fi
echo $cmts
ifIndex=$2
echo "Checking $cmts Interface $ifIndex history"
Lines=`snmptable -m ALL -v2c -cprivate $cmts cmtscmstatustable | grep registrationComplete`
IFS=$'\n'
> $workingDir/modems  ## Makes the file empty

for Line in $Lines
        do
        MAC=$(echo  $Line | awk '{print $1}')
        IP=$(echo $Line | awk '{print $2}')
        USIF=$(echo $Line | awk '{print $4}')
        if [ $USIF -eq $ifIndex -o $ifIndex -eq 0 ]; then      ## 1st if
                #echo -n $IP,
                echo $cmts,$ifIndex,$MAC >> modems
        fi
done
mkdir -p $workingDir/$cmts
#cat $workingDir/modems
copyDir=$modemdata/$cmts
scp -q root@10.1.1.51://$copyDir/*1808* $workingDir/$cmts/

## Generate a history file for each mac in $modems
while read modem ; do
	mac=$(echo $modem  | awk -F ',' '{print $3}')
	#echo Grepping $mac
	grep -hnw $mac  $workingDir/$cmts/*1808* > $workingDir/$cmts/$mac.history
	python analyseUpstreamData.py  $cmts $mac.history
done < modems
#rm -f  $workingDir/$cmts/*.history
