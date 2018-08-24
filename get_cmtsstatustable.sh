#!/bin/bash
workingDir=/opt/analyseUpstreamData
 cmts=$1
 ifIndex=$2
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
cat $workingDir/modems
