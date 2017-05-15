#!/usr/bin/python
# Copyright (c) Logicc Sytems Ltd.
# Author: David Jenkins

import sys
import time
import subprocess
import os
import requests
import settings

try:
  # read settings from settings.py
  verbose = settings.VERBOSE
  serial = settings.PI_KEY
except Exception, e:
  print __name__ + ": Could not read settings"
  print e
  sys.exit(1)

# Initialise
def initialise():
  os.system('modprobe w1-gpio')  # Activate GPIO module
  os.system('modprobe w1-therm') # Activate Temperature module
#  os.system('clear') # clear screen

# scans through /sys/devices to find 1wire files (active sensors) and save results to list
def findProbes(probes=''):
  findCMD = 'find /sys/devices/ -name "w1_slave"'
  out = subprocess.Popen(findCMD,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  # Get standard out and error
  (stdout, stderr) = out.communicate()
  probes = stdout.decode().split()
  return (probes)

# reads a file in filesystem
def readFile(file):
  tempfile = open(file)
  thetext = tempfile.read()
  tempfile.close()
  return(thetext)

def readProbes():
  probes = ''
  probesData = []
  probes=findProbes()
  for probe in probes:
    probeData = readFile(probe)
    probeID = probe.split("/")[4]
    tempdata = probeData.split("\n")[1].split(" ")[9]
    temperature = float(tempdata[2:]) / 1000
    probeNum =  str(probes.index(probe)+1)
    probesData.append((str(probeID)+'@'+str(serial),temperature,'temperature'))
    if verbose:
      print "Probe " + probeNum + " (id: " + probeID + ") Current Temperature is " + str(temperature) + " C"
  return probesData

# initialise
initialise()


