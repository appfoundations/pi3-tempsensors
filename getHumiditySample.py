#!/usr/bin/python
# Copyright (c) 2017 Logicc Systems Ltd.
# Author: Tony DiCola
# Bases on AdafruitDHT - thanks guys!

import sys
import Adafruit_DHT
import settings
import sqlite3

try:
    DHT_V = settings.DHT_V
    DHT_PIN = settings.DHT_PIN
    DB_NAME = settings.DB_NAME
except:
    print "Could not read settings"
    sys.exit(1)

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(DHT_V, DHT_PIN)

# Un-comment the line below to convert the temperature to Fahrenheit.
# temperature = temperature * 9/5.0 + 32

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)

try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    t = ('PI_KEY',)
    c.execute('SELECT value FROM params WHERE name=?', t)
    serial = c.fetchone()[0]
    db_entry = [(str('DHT11')+'@'+str(serial),temperature,'temperature'),
                (str('DHT11')+'@'+str(serial),humidity,'humidity')]
    c.executemany("INSERT INTO measure (time,probeId,measure, type) VALUES (CURRENT_TIMESTAMP,?,?,?)", db_entry)
    conn.commit()
    conn.close()
except  Exception, e:
    print e
    print "Could not save to DB"