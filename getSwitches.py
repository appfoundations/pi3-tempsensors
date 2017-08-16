#!/usr/bin/python
# Copyright (c) 2017 Logicc Systems Ltd.
# Author: Andre Neto
# Bases on script by Alex Eames http://RasPi.tv  
# http://raspi.tv/?p=6791  
  
import RPi.GPIO as GPIO  
import settings
import sys

try:
    verbose = settings.VERBOSE
    serial = settings.PI_KEY
except Exception, e:
    print __name__ + ": Could not read settings"
    print e
    sys.exit(1)

try:
    DOOR_PINS = settings.DOOR_PINS
except:
    if verbose:
        print 'set DOOR_PINS = []'
    DOOR_PINS = []


GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
for i, pin in enumerate(DOOR_PINS):
    GPIO.setup(pin, GPIO.IN)    # set pin (GPIO.BCM number) as input (button)  

def readSwitches():
    values = []
    for i, pin in enumerate(DOOR_PINS):
        value = 'OPEN' if GPIO.input(pin) else 'CLOSED'
        values.append(('Door-'+str(pin)+'@'+str(serial),value,'door'))
    return values
