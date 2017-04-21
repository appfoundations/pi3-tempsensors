#!/usr/bin/python
# Copyright (c) 2017 Logicc Systems Ltd.
# Author: Andre Neto
  
import time
import subprocess
import os
import requests
import settings
import sqlite3

def postData(data):
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    payload = {"id":data[0],"time": data[1], "probeID": data[2],"value": data[3], "type":data[4]}
    response = requests.request("POST", url, data=payload, headers=headers)

    # Show additional info for troubleshooting
    if verbose:
        print "Posted to API : " + str(payload) + "Response - " + str(response.status_code)
        print response.text
    return response.status_code

try:
    DB_NAME = settings.DB_NAME
    url = settings.URL
    apipost = settings.APIPOST
    verbose = settings.VERBOSE
except:
    print "Could not read settings"
    sys.exit(1)


try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    t = ('measure',)
    c.execute('SELECT table_idx FROM read_idx WHERE table_name=?',t)
    last_idx = c.fetchone()[0]
    print last_idx

    t = (int(last_idx),)
    c.execute('SELECT * FROM measure WHERE idx>?', t)
    measures = c.fetchall()
    #print measures

except  Exception, e:
    print e
    print "Could read from DB"

for mm in measures:
    print mm
    rr = postData(mm)
    if rr == 200
        last_idx = int(mm[0])
    else
        sys.exit(1)

try:
    t = (last_idx, 'measure',)
    c.execute('UPDATE read_idx SET table_idx = ?  WHERE table_name=? ',t)
    conn.commit()
    c.close()
    conn.close()
except  Exception, e:
    print e
    print "Could not close connection to DB"
