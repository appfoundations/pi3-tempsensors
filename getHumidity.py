#!/usr/bin/python
# Copyright (c) 2017 Logicc Systems Ltd.
# 
# Bases on AdafruitDHT - thanks guys!

import sys
import Adafruit_DHT
import settings
import pickle
from time import sleep

try:
    verbose = settings.VERBOSE
    DHT_V = settings.DHT_V
    serial = settings.PI_KEY
except Exception, e:
    print __name__ + ": Could not read settings"
    print e
    sys.exit(1)

try:
    DHT_PINS = settings.DHT_PINS
except:
    if verbose:
        print 'set DHT_PINS = []'
    DHT_PINS = []



# Try to grab a sensor reading.
def readDHT(avgOnly):

    try:
        f = open('pcklFiles/lastDHTValues.pckl', 'rb')
        lastDHTValues = pickle.load(f)
        f.close()
        if verbose:
            print 'last DHT values:'
            print lastDHTValues
            print ''
    except Exception, e:
        print e
        print 'failed to read DHT values'
        lastDHTValues = {}


    values=[]
    for i, pin in enumerate(DHT_PINS):
        for num in range(1,5):
            humidity, temperature = Adafruit_DHT.read(DHT_V, pin)
            if humidity is not None and temperature is not None and humidity < 120:
                if verbose:
                    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
                break
            sleep(2) 
        if humidity < 120:
            if pin not in lastDHTValues:
                lastDHTValues[str(pin)] = {}
                lastDHTValues[str(pin)]['humidity'] = []
                lastDHTValues[str(pin)]['temperature'] = []

            lastDHTValues[str(pin)]['humidity'].append(humidity)
            lastDHTValues[str(pin)]['temperature'].append(temperature)

    
    if not avgOnly:
        if verbose:
            print "Calc avg to return data"

        for pin, data in lastDHTValues.iteritems():
            avg = sum(data['humidity']) / float(len(data['humidity']))
            humidity = round(avg,3)
            avg = sum(data['temperature']) / float(len(data['temperature']))
            temperature = round(avg,3)

            values.append(('H-'+str(pin)+'@'+str(serial),humidity,'humidity'))
            values.append(('T-'+str(pin)+'@'+str(serial),temperature,'temperature'))
        lastDHTValues = {}

    try:
        f = open('pcklFiles/lastDHTValues.pckl', 'wb')
        pickle.dump(lastDHTValues, f)
        f.close()
    except Exception, e:
        print e
        print 'failed to save DHT values'


    return values


