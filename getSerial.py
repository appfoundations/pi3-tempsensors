#!/usr/bin/python
# Copyright (c) Logicc Sytems Ltd.
# Author: David Jenkins
#
# Description : Grabs unique serial number from the Raspberry PI processor from /proc/cpuinfo, use so we know sensors are connect to this device.

import re
import sqlite3
import settings

DB_NAME = settings.DB_NAME

### Functions ###

def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    r = re.compile('0[0-9abcdef]+')
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = r.findall(line)[0].lstrip("0")
    f.close()
  except:
    cpuserial = "ERROR000000000"
 
  return cpuserial

### Program Loop ###

serial = getserial()
print serial

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()
db_entry = ('PI_KEY', 'STRING', serial)
c.execute("INSERT OR REPLACE INTO params (name,type,value) VALUES (?,?,?)", db_entry)
conn.commit()
conn.close()
