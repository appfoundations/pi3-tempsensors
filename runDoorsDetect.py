#!/usr/bin/python
# Copyright (c) 2017 Logicc Systems Ltd.
# Author: Andre Neto
# Bases on script by Alex Eames http://RasPi.tv  
# http://raspi.tv/?p=6791  
  
import RPi.GPIO as GPIO  
from time import sleep
import sqlite3
import datetime
import pickle


try:
    import putDataDB
    import settings
    import setWarning
except  Exception, e:
    print e
    print __name__ + ": Could not perform import"
    sys.exit(1)

try:
    DOOR_PINS = settings.DOOR_PINS
    DB_NAME = settings.DB_NAME
    serial = settings.PI_KEY
    verbose = settings.VERBOSE
    WARNING = settings.WARNING
    MAX_OPEN_TIME = settings.MAX_OPEN_TIME
except:
    print "Could not read settings"
    sys.exit(1)

GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
doorsData = {}

def update_lastStatusRecord (entry):
    entry = entry + (datetime.datetime.now(),)
    try:
        f = open('lastDoorStatus.pckl', 'rb')
        lastDoorStatus = pickle.load(f)
        f.close()
        if verbose:
            print 'last door status'
            print lastDoorStatus
            print
    except:
        lastDoorStatus = {}

    try:
        lastDoorStatus[entry[0]]
    except:
        lastDoorStatus[entry[0]] = entry

    if lastDoorStatus[entry[0]][1] != entry[1]:
        lastDoorStatus[entry[0]] = entry

    try:
        f = open('lastDoorStatus.pckl', 'wb')
        pickle.dump(lastDoorStatus, f)
        f.close()
    except Exception, e:
        print e
        print 'failed to save last door status'


# Define a threaded callback function to run in another thread when events are detected  
def my_callback(channel):
    sleep(2)
    value = 'OPEN' if GPIO.input(channel) else 'CLOSED'
    entry = [('Door-'+str(channel)+'@'+str(serial), value, 'door')]
    global doorsData
    doorsData[entry[0][0]] = entry[0]
    if verbose:
        print entry[0]
        print
    putDataDB.postData(entry)
    if WARNING:
        update_lastStatusRecord(entry[0])
        print '\tset Warning'
        setWarning.setWarn(entry)
        

# get an initial value from doors status
for i, pin in enumerate(DOOR_PINS):
    GPIO.setup(pin, GPIO.IN)    # set GPIO25 as input (button)  
    my_callback(pin)

# when a changing edge is detected on port 25, regardless of whatever   
# else is happening in the program, the function my_callback will be run  
for i, pin in enumerate(DOOR_PINS):
    GPIO.add_event_detect(pin, GPIO.BOTH, callback=my_callback, bouncetime=500)  
  
try:
    while 1:
        sleep(MAX_OPEN_TIME)         # wait MAX_OPEN_TIME seconds  
        if WARNING:
            print '\tset Warning'
            setWarning.setWarn(doorsData.values())

except Exception,e:
    print e
    print "Interrupted"
  
finally:                   # this block will run no matter how the try block exits  
    GPIO.cleanup()         # clean up after yourself  
