#!/bin/sh

#function to downlaod urls.
#When download fails, retries 30 seconds later.
#Nasa server usually only accept a few downloads parallel.
fetch_urls() {
	iteration=0
	DONE=false
	until $DONE; do
		read line || DONE=true
		echo "$iteration is loading $line"	
		#filtering for only ND (nadir) files. Change this to also accept other files
		if [[ $line == *"L1bScND"* ]]; then
			line=${line%$'\r'}
			until $(curl -b ~/.urs_cookies -c ~/.urs_cookies -L -n -f -Og $line); do
			    printf '.'
			    sleep 30
			done
		fi
		((iteration++))
	done;
}

#the passed arguments and changes folder
filename="$1"
folder="$2"
echo "changes folder $folder"
cd $folder

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
