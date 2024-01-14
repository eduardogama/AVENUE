#!/bin/bash


## Function that will get executed when the user presses Ctrl+C
#function handler(){
#    echo "Processing the Ctrl+C"
#    echo "Parameters of experiment "
#}

## Assign the handler function to the SIGINT signal
#trap handler SIGINT

users=(10 20 30 40 50)
filename=sim.$(date "+%Y.%m.%d-%H.%M.%S")
round=0

for k in $(seq 1 5);
do
    for u in "${users[@]}";
    do
        # Simulation progress
        echo "$round $k $u" >> $filename
        
        # Download Chrome
        python users/download-chrome.py
        
        echo "python mininet/icc-scenario.py --seed=$round --users=$u"
        # Start Simulation
        python mininet/icfec-scenario.py --seed=$round --users=$u
        

        # Cleanup
        mn -c
        pkill xterm
        pkill chrome

        round=$((round+1))
    done
done
