#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

import sys
import time
import RPi.GPIO as GPIO

global state
global lastState
state=''
lastState=''

GPIO.setmode(GPIO.BCM)
 
if len(sys.argv) == 2:
    pin = int(sys.argv[1])
else:
    print('usage: sudo ./monitorDoors.py {GPIOpin#}')
    print('eg: sudo ./monitorDoors.py 23 - Read from PIO #23')
    sys.exit(1)


GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # activate input with PullUp

def init_state():
    # Store initial state
    state = GPIO.input(pin) 
    lastState = GPIO.input(pin) 
    print_state()
    return


def print_state():
    if state:
        print "Door is OPEN"
    else:
        print "Door is CLOSED"
    return

def monitor_state():
    state=GPIO.input(pin) 
    if lastState != state:
        print_state()
    lastState=state
    time.sleep(0.1)



init_state()
print_state()

#monitor_state() <-- at some point move the code below into function

while True:
    state=GPIO.input(pin) 
    if lastState != state:
        print_state()
    lastState=state
    time.sleep(0.1)


