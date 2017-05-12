#!/usr/bin/python
# Copyright (c) 2017 Logicc Systems Ltd.
# Author: Andre Neto
# Bases on script by Alex Eames http://RasPi.tv  
# http://raspi.tv/?p=6791  
  
import RPi.GPIO as GPIO  
from time import sleep
import settings
import sqlite3

try:
    DOOR_PINS = settings.DOOR_PINS
    DB_NAME = settings.DB_NAME
except:
    print "Could not read settings"
    sys.exit(1)

GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
for i, pin in enumerate(DOOR_PINS):
    GPIO.setup(pin, GPIO.IN)    # set GPIO25 as input (button)  
  
# Define a threaded callback function to run in another thread when events are detected  
def my_callback(channel):  
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        t = ('PI_KEY',)
        c.execute('SELECT value FROM params WHERE name=?', t)
        serial = c.fetchone()[0]
        value = 'OPEN' if GPIO.input(channel) else 'CLOSE'
        db_entry = (str(channel)+'@'+str(serial), value, 'door')
        c.execute("INSERT INTO measure (time,probeId,measure, type) VALUES (datetime('now', 'localtime'),?,?,?)", db_entry)
        conn.commit()
        conn.close()
        print str(value)+'@'+str(channel)
    except  Exception, e:
        print e
        print "Could not save to DB"
  
# when a changing edge is detected on port 25, regardless of whatever   
# else is happening in the program, the function my_callback will be run  
for i, pin in enumerate(DOOR_PINS):
    my_callback(pin)  
