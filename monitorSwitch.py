#!/usr/bin/env python2.7  
# script by Alex Eames http://RasPi.tv  
# http://RasPi.tv/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3  
import RPi.GPIO as GPIO  
import time, sys

# Read PIN from args
if len(sys.argv) == 2:
    pin = int(sys.argv[1])
else:
    print('usage: sudo ./monitorSwitch.py {GPIOpin#}')
    print('eg: sudo ./monitorSwitch.py 23 - Read from PIO #23')
    sys.exit(1)

def pin_state():
    state=GPIO.input(pin) 
    if state:
        print "Switch OPEN"
    else:
        print "Switch CLOSED"
    return

# Define threaded callback functions - to run in another thread when events are detected and print current switch state
def my_callback(channel):  
    pin_state()
  
# GPIO - Setup and get pin ready for input, pulled up to avoid false detection.  
GPIO.setmode(GPIO.BCM)  
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

# Add events for state changes on GPIO pins, both rising and falling edge events.
GPIO.add_event_detect(pin, GPIO.BOTH, callback=my_callback, bouncetime=300)  

# Keep running for ever
while True:
    time.sleep(60) # 2 second delay


