#!/usr/bin/python
# Copyright (c) Logicc Sytems Ltd.
# Author: David Jenkins

import sys
import time
import subprocess
import os
import requests
import settings
import pickle

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

def readProbes(avgOnly):

  try:
    f = open('pcklFiles/lastTemperatureValues.pckl', 'rb')
    lastTempValues = pickle.load(f)
    f.close()
    if verbose:
      print 'last temperature values:'
      print lastTempValues
      print ''
  except Exception, e:
    print e
    print 'failed to read temperature values'
    lastTempValues = {}

  probes = ''
  probesData = []
  probes=findProbes()
  for probe in probes:
    probeData = readFile(probe)
    probeID = probe.split("/")[4]
    tempdata = probeData.split("\n")[1].split(" ")[9]
    temperature = float(tempdata[2:]) / 1000
    probeNum =  str(probes.index(probe)+1)

    if temperature < 50:
      if str(probeID) not in lastTempValues:
        lastTempValues[str(probeID)] = []

      lastTempValues[str(probeID)].append(temperature)
      if verbose:
        print "Probe " + probeNum + " (id: " + probeID + ") Current Temperature is " + str(temperature) + " C"

    else:
      if str(probeID) in lastTempValues:
        lastIdx = len(lastTempValues[str(probeID)]) - 1
        temperature = lastTempValues[str(probeID)][lastIdx]
        lastTempValues[str(probeID)].append(temperature)
        if verbose:
          print "FROM LAST VALUES:"
          print "\tProbe " + probeNum + " (id: " + probeID + ") Current Temperature is " + str(temperature) + " C"
      else:
        if verbose:
          print "SKIPED: Probe " + probeNum + " (id: " + probeID + ") Current Temperature is " + str(temperature) + " C"
  

  if not avgOnly:
    if verbose:
      print "Calc avg to return temperature"
    probeNum = 0;
    for probeID, values in lastTempValues.iteritems():
      probeNum += 1
      avg = sum(values) / float(len(values))
      temperature = round(avg,3)
      probesData.append((str(probeID)+'@'+str(serial),temperature,'temperature'))
      if verbose:
        print "Probe " + str(probeNum) + " (id: " + str(probeID) + ") Current Temperature is " + str(temperature) + " C"
    lastTempValues = {}

  try:
    f = open('pcklFiles/lastTemperatureValues.pckl', 'wb')
    pickle.dump(lastTempValues, f)
    f.close()
  except Exception, e:
    print e
    print 'failed to save temperature values'
  
  return probesData

# initialise
initialise()


