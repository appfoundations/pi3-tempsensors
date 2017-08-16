#!/usr/bin/python
# Copyright (c) 2017 Logicc Systems Ltd.
# Author: Andre Neto
# Bases on script by Alex Eames http://RasPi.tv  
# http://raspi.tv/?p=6791  
  
import RPi.GPIO as GPIO  
import settings
import sys
from time import sleep
import pickle
import subprocess
import datetime

try:
    verbose = settings.VERBOSE
    serial = settings.PI_KEY
    BUTTON_MIN_INTERVAL = settings.BUTTON_MIN_INTERVAL
    MAX_OPEN_TIME = settings.MAX_OPEN_TIME
    TEMP_WARN_DELAY = settings.TEMPERATURE_WARN_DELAY
except Exception, e:
    print __name__ + ": Could not read settings"
    print e
    sys.exit(1)

try:
    import putWarnAPI
except Exception, e:
    print __name__ + ": Could not perform imports"
    print e
    sys.exit(1)

GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  

def setWarn( data ):
    try:
        f = open('pcklFiles/buttonLastCall.pckl', 'rb')
        last = pickle.load(f)
        f.close()
        diff = (datetime.datetime.now() - last).total_seconds()
        if verbose:
            print 'read last button call time'
            print last
            print 'minutes since last button call'
            print diff
    except:
        diff = BUTTON_MIN_INTERVAL + 100
        if verbose:
            print 'no record from button call'

    if diff < BUTTON_MIN_INTERVAL:
        if verbose:
            print 'time since last button call not enough'
        return

    try:
        f = open('pcklFiles/pcklFiles/limits.pckl', 'rb')
        limits = pickle.load(f)
        f.close()
        if verbose:
            print 'configured limits'
            print limits
            print ''
    except:
        limits = None


    try:
        f = open('pcklFiles/lastDoorStatus.pckl', 'rb')
        lastDoorStatus = pickle.load(f)
        f.close()
        if verbose:
            print 'last door status'
            print lastDoorStatus
            print ''
    except:
        lastDoorStatus = None

    try:
        f = open('pcklFiles/temperatureStatus.pckl', 'rb')
        temperatureStatus = pickle.load(f)
        f.close()
        if verbose:
            print 'temperature sensors status'
            print temperatureStatus
            print ''
    except:
        temperatureStatus = {}

    warnList = []
    multiMsg = ''
    sensorIds = []
    for item in data:
        limit = None
        warn  = None
        delta = None

        if item[2] == 'temperature':
            if verbose:
                print 'temperature item:'
                print item
            try:
                limit = limits[item[0]]
                print limit
            except:
                limit = None
                
            if limit is not None and (item[1] > float(limit['max'])):
                warn = 'tempAbove'
                msg = 'Warning! Temperature Above Acceptable Levels (' + str(item[1]) + ' > ' + str(limit['max']) + ' - ' + item[0] + ')'
            elif limit is not None and (item[1] < float(limit['min'])):    
                warn = 'tempBelow'
                msg = 'Warning! Temperature Below Acceptable Levels (' + str(item[1]) + ' < ' + str(limit['min']) + ' - ' + item[0] + ')'
            else:
                warn = None

            if warn is None:
                temperatureStatus[item[0]] = None
            else:
                try:
                    temperatureStatus[item[0]]
                    if temperatureStatus[item[0]] is not None:
                        delta = (datetime.datetime.now() - temperatureStatus[item[0]]).total_seconds()
                        msg = msg + '<br/>'
                        msg = msg + 'Deviation started at ' + temperatureStatus[item[0]].strftime('%d/%m/%Y %H:%M:%S')
                    else:
                        delta = None
                except:
                    delta = None

                if delta is None:
                    warn = None
                    temperatureStatus[item[0]] = datetime.datetime.now()
                elif delta < TEMP_WARN_DELAY:
                    warn = None
                else:
                    warnList.append(warn)
                    multiMsg = multiMsg + msg + '<br/> ' + '<br/> '
                    sensorIds.append(item[0])

            if verbose:
                print 'start alarm delta:'
                print delta

            try:
                f = open('pcklFiles/temperatureStatus.pckl', 'wb')
                pickle.dump(temperatureStatus, f)
                f.close()
            except Exception, e:
                print e
                print 'failed to save temperature status'

        elif item[2] == 'door':
            if verbose:
                print 'door item:'
                print item
            try:
                lastStatus = lastDoorStatus[item[0]]
                diff = (datetime.datetime.now() - lastStatus[3]).total_seconds()
                if verbose:
                    print 'limit: ' 
                    print MAX_OPEN_TIME
                    print 'seconds in current status'
                    print diff
                    print 'door current status:'
                    print item[1]
            except Exception,e:
                print e
                diff = 0

            if item[1] == 'OPEN' and diff > ( MAX_OPEN_TIME ) :
                warn = 'doorOpen'
                warnList.append(warn)
                msg = 'Warning! Door open for more than acceptable time (' + str(int(diff)) + 'sec > ' + str(MAX_OPEN_TIME) + 'sec - ' + item[0] + ')'
                msg = msg + '<br/>'
                msg = msg + 'Door open since ' + lastStatus[3].strftime('%d/%m/%Y %H:%M:%S')
                multiMsg = multiMsg + msg + '<br/> ' + '<br/> '
                sensorIds.append(item[0])
            else:
                warn = None


    if len(warnList) > 0:
        if verbose:
            print 'setting warning'
        # check if sound play is ON
        grepCMD = "ps -ef | grep setSiren | grep -v grep"
        setSirenCMD = ['python', 'setSiren.py']
        for i, ww in enumerate(warnList):
            setSirenCMD.append('-w')
            setSirenCMD.append(ww)

        pp = subprocess.Popen(grepCMD,shell=True,stdout=subprocess.PIPE)
        if pp.communicate()[0] == '':
            # if play is OFF - start play (backend/new thread)
            subprocess.Popen(setSirenCMD)
            # send warning email - inside play check to avoid high volume of mails
            putWarnAPI.postWarn(sensorIds, multiMsg)
        else:
            if verbose:
                print 'setSiren is RUNNING'
                print ''
        return True
        
    return False
