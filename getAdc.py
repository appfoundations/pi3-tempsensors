# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time
import sys

import Adafruit_MCP3008 as Adafruit
import settings
import sqlite3

try:
    CLK = settings.CLK
    MISO = settings.MISO
    CS = settings.CS
    MOSI = settings.MOSI
    verbose = settings.VERBOSE
    serial = settings.PI_KEY
except Exception, e:
    print __name__ + ": Could not read settings"
    print e
    sys.exit(1)

try:
    ADC_CHANNELS = settings.ADC_CHANNELS
except:
    if verbose:
        print 'set ADC_CHANNELS = []'
    ADC_CHANNELS = []


mcp = Adafruit.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

def readCT():
    values=[]
    for i, pin in enumerate(ADC_CHANNELS):
        value = '{0:0.1f}'.format(mcp.read_adc(pin) * 3.3 / 1024 * 20)
        values.append(('CT-'+str(pin)+'@'+str(serial),value,'current'))
    return values

