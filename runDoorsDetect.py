#!/usr/bin/python
# Copyright (c) 2017 Logicc Systems Ltd.
# Author: Andre Neto
# Bases on script by Alex Eames http://RasPi.tv  
# http://raspi.tv/?p=6791  
  
import RPi.GPIO as GPIO  
from time import sleep
import sqlite3


try:
    import putDataDB
    import settings
except  Exception, e:
    print e
    print __name__ + ": Could not perform import"
    sys.exit(1)

try:
    DOOR_PINS = settings.DOOR_PINS
    DB_NAME = settings.DB_NAME
    serial = settings.PI_KEY
    verbose = settings.VERBOSE
except:
    print "Could not read settings"
    sys.exit(1)

GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
for i, pin in enumerate(DOOR_PINS):
    GPIO.setup(pin, GPIO.IN)    # set GPIO25 as input (button)  
  
# Define a threaded callback function to run in another thread when events are detected  
def my_callback(channel):
    value = 'OPEN' if GPIO.input(channel) else 'CLOSE'
    entry = [(str(channel)+'@'+str(serial), value, 'door')]
    if verbose:
        print entry[0]
    putDataDB.postData(entry)
  
# when a changing edge is detected on port 25, regardless of whatever   
# else is happening in the program, the function my_callback will be run  
for i, pin in enumerate(DOOR_PINS):
    GPIO.add_event_detect(pin, GPIO.BOTH, callback=my_callback, bouncetime=500)  
  
try:
    while 1:
        sleep(30)         # wait 60 seconds  

except:
    print "Interrupted"
  
finally:                   # this block will run no matter how the try block exits  
    GPIO.cleanup()         # clean up after yourself  
