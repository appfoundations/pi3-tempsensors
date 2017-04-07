#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

import sys
import time
import RPi.GPIO as io
io.setmode(io.BCM)
 

#print "Arg 0: "+str(sys.argv[0])
#print "Arg 1: "+str(sys.argv[1])

if len(sys.argv) == 2:
    door_pin = int(sys.argv[1])
else:
    print('usage: sudo ./monitorDoors.py {GPIOpin#}')
    print('eg: sudo ./monitorDoors.py 23 - Read from PIO #23')
    sys.exit(1)

#io.setup(pir_pin, io.IN)         # activate input
io.setup(door_pin, io.IN, pull_up_down=io.PUD_UP)  # activate input with PullUp

count=0
while True:
    if io.input(door_pin):
    	count=count+1
        print("DOOR (Pin "+str(door_pin)+") OPEN!"+str(count))
    else:
    	print("DOOR 1 CLOSED")
    time.sleep(0.5)
