#!/usr/bin/python
# Copyright (c) 2017 Logicc Systems Ltd.
# Author: Andre Neto

import sys
import datetime

try:
    import getAdc
    import getTemps
    import getSwitches
    import getHumidity
    import putDataDB
    import putDataAPI
    import settings
    import setWarning
    import pickle
except  Exception, e:
    print e
    print "Main: Could not perform import"
    sys.exit(1)

try:
    serial = settings.PI_KEY
    APIPOST = settings.APIPOST
    verbose = settings.VERBOSE
    WARNING = settings.WARNING
    SAMPLING_PERIOD = settings.SAMPLING_PERIOD
    APIPOST_PERIOD = settings.APIPOST_PERIOD
except Exception, e:
    "Main: Could not read settings"
    print e
    sys.exit(1)

try:
    f = open('pcklFiles/lastEventsTime.pckl', 'rb')
    lastEventsTime = pickle.load(f)
    f.close()
    lastSampleTime = lastEventsTime['sample']
    lastPostTime = lastEventsTime['post']
    if verbose:
      print 'last events time:'
      print lastEventsTime
      print ''
except Exception, e:
    print e
    print 'failed to read last events time'
    lastEventsTime = {}
    lastEventsTime['sample'] = (datetime.datetime.now() - datetime.timedelta(minutes=SAMPLING_PERIOD))
    lastSampleTime = lastEventsTime['sample']
    lastEventsTime['post'] = (datetime.datetime.now() - datetime.timedelta(minutes=APIPOST_PERIOD))
    lastPostTime = lastEventsTime['post']

data = []

print "Begin master.py"
print datetime.datetime.now().strftime('%Y-%m-%d')
print datetime.datetime.now().strftime('%H:%M:%S')

currTime = datetime.datetime.now()
currMinute =currTime.minute

lastSampleMinute = lastSampleTime.minute
lastPostMinute = lastPostTime.minute

if lastSampleMinute > currMinute:
    lastSampleMinute = lastSampleMinute - 60

if lastPostMinute > currMinute:
    lastPostMinute = lastPostMinute - 60

#### Determine if is time to sample and post data #####
if (currMinute - lastSampleMinute) < SAMPLING_PERIOD:
    if verbose:
        print "Time since last sampling not enough ("+ str(currMinute - lastSampleMinute) + " < " + str(SAMPLING_PERIOD) + ")"
    sys.exit(0)
else:
    if verbose:
        print "It's time for some data sampling ("+ str(currMinute - lastSampleMinute) + " >= " + str(SAMPLING_PERIOD) + ")"

if (currMinute - lastPostMinute) < APIPOST_PERIOD:
    avgOnly = True
    if verbose:
        print "Time since last sampling not enough ("+ str(currMinute - lastPostMinute) + " < " + str(APIPOST_PERIOD) + ")"
else:
    avgOnly = False
    if verbose:
        print "It's time for some API posting ("+ str(currMinute - lastPostMinute) + " >= " + str(APIPOST_PERIOD) + ")"

#### Read CTs data #####
if not avgOnly:
    print datetime.datetime.now().strftime('%H:%M:%S')
    print '\tRead CTs - ADC_CHANNELS'
    ctData = getAdc.readCT()
    if verbose:
        print ctData
    data.extend(ctData)
else:
    if verbose:
        print datetime.datetime.now().strftime('%H:%M:%S')
        print '\tDo not read CTs if not posting to API'


#### Read Temperature data #####
print datetime.datetime.now().strftime('%H:%M:%S')
print '\tRead Temps - OneWire'
temps = getTemps.readProbes(avgOnly)
if verbose:
    print temps
data.extend(temps)

#### Read Switches data #####
if not avgOnly:
    print datetime.datetime.now().strftime('%H:%M:%S')
    print '\tRead Switches - DOOR_PINS'
    switches = getSwitches.readSwitches()
    if verbose:
        print switches
    data.extend(switches)
else:
    if verbose:
        print datetime.datetime.now().strftime('%H:%M:%S')
        print '\tDo not read switches if not posting to API'

#### Read DHT data #####
print datetime.datetime.now().strftime('%H:%M:%S')
print '\tRead DHT - DHT_PINS'
dhts = getHumidity.readDHT(avgOnly)
if verbose:
    print dhts
data.extend(dhts)

print datetime.datetime.now().strftime('%H:%M:%S')
print '\tsave to DB'
putDataDB.postData(data)

lastEventsTime['sample'] = currTime
lastEventsTime['post'] = currTime if not avgOnly else lastEventsTime['post']

try:
    f = open('pcklFiles/lastEventsTime.pckl', 'wb')
    pickle.dump(lastEventsTime, f)
    f.close()
except Exception, e:
    print e
    print 'failed to save last events time'

print datetime.datetime.now().strftime('%H:%M:%S')

if APIPOST:
    print '\tpost to API'
    putDataAPI.postDBData()
    print datetime.datetime.now().strftime('%H:%M:%S')

if APIPOST:
    temp = int(datetime.datetime.now().strftime('%H%M'))
    if temp < 10:
        print '\tclean old Data from DB'
        putDataDB.cleanData()
        print datetime.datetime.now().strftime('%H:%M:%S')

if WARNING:
    print '\tset Warning'
    setWarning.setWarn(data)
    print datetime.datetime.now().strftime('%H:%M:%S')

print "End master.py"
print

