#!/bin/bash

# This script starts Python program from file "main.py"
# In a loop it checks since when a Raspberry Pi was turned on.
# After at least 48 hours and at 22 PM a Raspberry Pi will reboot.

sudo python3 /home/pi/tannery/main.py &



while true; do
	sinceTime=$(awk '{print int($0/60/60/24); }' /proc/uptime)
	echo "$sinceTime"
	if [ "$sinceTime" -ge 2 ]; then
		while true; do
			eveningHour=`date +%H`
			if [ "$eveningHour" -ge 22 ]; then 
				sudo reboot now
			fi 
		done

	fi
done
