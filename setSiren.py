#!/usr/bin/python
# Copyright (c) 2017 Logicc Systems Ltd.
# Author: Andre Neto
  
import RPi.GPIO as GPIO  
from time import sleep
import subprocess
import time 
import getopt
import sys
import datetime
import pickle

try:
    import settings
except  Exception, e:
    print e
    print __name__ + ": Could not perform import"
    sys.exit(1)

try:
    CLEAR_WARN_PIN = settings.CLEAR_WARN_PIN
    verbose = settings.VERBOSE
    MAX_TIME = settings.MAX_TIME_SOUND

    tempAboveAudio = settings.TEMP_ABOVE_AUDIO_FILE
    tempBelowAudio = settings.TEMP_BELOW_AUDIO_FILE
    doorOpenAudio = settings.DOOR_OPEN_AUDIO_FILE
except:
    print "Could not read settings"
    sys.exit(1)

GPIO.setmode(GPIO.BCM)
warnTypes = ['tempAbove', 'tempBelow', 'doorOpen']
warn = []
player = None
done = False

# Define a threaded callback function
def my_callback(channel):
    if GPIO.input(channel):
        if verbose:
            print 'Button pressed'
        if player.poll() is None:
            player.stdin.write("q")
        try:
            last = datetime.datetime.now()
            f = open('pcklFiles/buttonLastCall.pckl', 'wb')
            pickle.dump(last, f)
            f.close()
        except Exception as e:
            print e
        sys.exit()

def main(argv):
    global warn
    global warnTypes
    global player
    try:
        opts, args = getopt.getopt(argv,"hw:",["warn="])
    except getopt.GetoptError:
        print 'setSiren.py -w <warnType>'
        sys.exit(2)

    if len(opts) == 0:
        print 'setSiren.py -w <warnType>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'setSiren.py -w <warnType>'
            sys.exit()
        elif opt in ("-w", "--warn"):
            if arg in warnTypes and arg not in warn:
                warn.append( arg)

     
    
    if len(warn) > 0 :
        done = False
        GPIO.setup(CLEAR_WARN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(CLEAR_WARN_PIN, GPIO.BOTH, callback=my_callback, bouncetime=50)
    else:
        done = True

    initTime = datetime.datetime.now()

    while(not done):
        for i, type in enumerate(warn):
            wait = True
            if   type == 'tempAbove':
                audioFile = tempAboveAudio
            elif type == 'tempBelow':
                audioFile = tempBelowAudio
            elif type == 'doorOpen':
                audioFile = doorOpenAudio

            try: 
                audioFile   
            except NameError:
                print "no audio file defined"
                sys.exit()
            else:
                player = subprocess.Popen(["omxplayer", audioFile, "-o", "local"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            while(wait):
                time.sleep( 2 )
                try:
                    if player.poll() is not None:
                        wait = False
                except IOError as e:
                    print e
                    
                if (datetime.datetime.now() - initTime).total_seconds() > MAX_TIME:
                    try:
                        if player.poll() is None:
                            player.stdin.write("q")
                    except IOError as e:
                        print e
                    sys.exit()


if __name__ == "__main__":
   main(sys.argv[1:])
