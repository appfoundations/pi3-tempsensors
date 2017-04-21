#!/usr/bin/python
# Copyright (c) Logicc Sytems Ltd.
# Author: David Jenkins

import time
import subprocess
import os
import requests
import settings
import sqlite3

try:
  # read settings from settings.py
  key = settings.KEY
  url = settings.URL
  apipost = settings.APIPOST
  verbose = settings.VERBOSE
  loop = settings.LOOP
  delay = settings.DELAY
  DB_NAME = settings.DB_NAME
except:
  print "Could not read settings"
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

# post data to DB
def postTemp():
  try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    t = ('PI_KEY',)
    c.execute('SELECT value FROM params WHERE name=?', t)
    serial = c.fetchone()[0]
    c.executemany("INSERT INTO measure (time,probeId,measure, type) VALUES (CURRENT_TIMESTAMP,? || '@"+str(serial)+"',?,'temperature')", probes_data)
    conn.commit()
    conn.close()
  except  Exception, e:
    print e
    print "Could not save to DB"

def readProbes():
  probes=""
  probes=findProbes()
  for probe in probes:
    probeData = readFile(probe)
    probeID = probe.split("/")[4]
    tempdata = probeData.split("\n")[1].split(" ")[9]
    temperature = float(tempdata[2:]) / 1000
    probeNum =  str(probes.index(probe)+1)
    print "Probe " + probeNum + " (id: " + probeID + ") Current Temperature is " + str(temperature) + " C"
    probes_data.append((probeID,temperature))
  print probes_data


# define vars
probes = ''
probes_data = []

# main program
initialise()
readProbes()
postTemp()

