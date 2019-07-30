#!/bin/sh

#define what month to download
declare -a monthlist=("18"*)

## download for every month in list
for month in "${monthlist[@]}"
do
        #create a detached screen for each month and call load.sh script for each month. 
        screen -d -m -S $"$month$i" 
        screen -R $"$month$i"  -X stuff $"echo '$month'\n"
        screen -R $"$month$i"  -X stuff $". ./load.sh list.txt $month/ \n"
done   
