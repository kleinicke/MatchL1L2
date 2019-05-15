#!/bin/sh

fetch_urls() {
	iteration = 0
	#while read -r line; do
	DONE=false
	until $DONE; do
		read line || DONE=true
		# you code
		echo "$iteration is loading $line"	
		if [[ $line == *"L1bScND"* ]]; then
			line=${line%$'\r'}
			until $(curl -b ~/.urs_cookies -c ~/.urs_cookies -L -n -f -Og $line); do
				printf '.'
				sleep 30
			done
					#curl -b ~/.urs_cookies -c ~/.urs_cookies -L -n -f -Og $line
		fi
		((iteration++))
	done;
}
#fetch_urls() {
#        while read -r line; do
#                curl -b ~/.urs_cookies -c ~/.urs_cookies -L -n -f -Og $line && echo || exit_with_error "Command failed with error. Please retrieve the data manually."
#        done;
#}
filename="$1"
#echo $filename
#cat filename | while read LINE; do
#    echo $LINE
#done
DONE=false
until $DONE; do
	read line || DONE=true
#while read -r line; do
    name="$line"
    echo "Name read from file - $name"
done < "$filename"
fetch_urls < "$filename"
#'EDSCEOF'
# Insert URLS here
#https://oco2.gesdisc.eosdis.nasa.gov/data/OCO2_DATA/OCO2_L2_Lite_FP.9r/2018/oco2_LtCO2_181030_B9003r_181130204140s.nc4
#https://oco2.gesdisc.eosdis.nasa.gov/data/OCO2_DATA/OCO2_L2_Lite_FP.9r/2018/oco2_LtCO2_181031_B9003r_181130204353s.nc4
#EDSCEOF
