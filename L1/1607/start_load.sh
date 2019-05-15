#split -l 100 subset_OCO2_L1B_Science_V8r_20190304_174240.txt --numeric-suffixes -a 3
for i in `seq -f "%03g" 0 4`;
        do
		
                screen -S $i -d -m
		screen -r $i  -X stuff $"echo '$i'\n"
		screen -r $i  -X stuff $"bash load.sh x$i\n"
		#screen -r $i  -X stuff $"bash load.sh x$i\n"
                
        done    
#screen -S 012 -d -m
#screen -r 012  -X stuff $"bash load.sh x012\n"
