#!/bin/sh
#month="1605"
declare -a monthlist=("1801" "1802" "1803" "1804" "1805" "1806" "1807" "1808" "1809" "1810" "1811" "1812")

##"1702" "1703" "1704" "1705" "1706" "1707" "1709" "1710" "1711" "1712")
## now loop through the above array
for month in "${monthlist[@]}"
do
        for i in `seq -f "%03g" 0 5`;
        do		
                        #screen  $"$month$i" -d -m
                        screen -d -m -S $"$month$i" 
                        screen -R $"$month$i"  -X stuff $"echo '$i'\n"
                        screen -R $"$month$i"  -X stuff $". ./load.sh x$i $month/ \n"
                        #screen -r $i  -X stuff $"bash load.sh x$i\n"
                        
        done 
done   
#screen -S 012 -d -m
#screen -r 012  -X stuff $"bash load.sh x012\n"


#split -l 100 --numeric-suffixes -a 3 subset_OCO2_L1B_Science_V8r_20190304_174240.txt 
