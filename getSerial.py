#!/usr/bin/python
# Copyright (c) Logicc Sytems Ltd.
# Author: David Jenkins
#
# Description : Grabs unique serial number from the Raspberry PI processor from /proc/cpuinfo, use so we know sensors are connect to this device.

### Functions ###

def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"
 
  return cpuserial

### Program Loop ###

print getserial()