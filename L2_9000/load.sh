#!/bin/sh

#function to downlaod urls.
#When download fails, retries 30 seconds later.
fetch_urls < "$filename"
fetch_urls() {
	iteration=0
	DONE=false
	until $DONE; do
		read line || DONE=true
		# you code
		echo "$iteration is loading $line"	
		#the commented line can be used to filter for certain filenames
		#if [[ $line == *"L1bScND"* ]]; then
        line=${line%$'\r'}
        if [[ $line ]]; then
            until $(curl -b ~/.urs_cookies -c ~/.urs_cookies -L -n -f -Og $line); do
                printf '.'
                sleep 30
            done
        fi
		((iteration++))
	done;
}

#first passed argument is the textfile with the names of the files to download
#filename="$1"
#or shorter just use this file
filename = "L2list.txt"

#iterates through the lines of the file and calls above function for each line.
DONE=false
iteration=0
until $DONE; do
	read line || DONE=true
    name="$line"
    echo "$iteration: Name read from file - $name"
    ((iteration++))
done < "$filename"
fetch_urls < "$filename"
