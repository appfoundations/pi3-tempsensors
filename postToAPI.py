#!/usr/bin/python
# Copyright (c) 2017 Logicc Systems Ltd.
# Author: Andre Neto
  
import time
import subprocess
import os
import requests
import settings
import sqlite3

def postData(key,data):
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    payload = {"key":api_key,"id":data[0],"datecollected": data[1], "probeid": data[2],"temp": data[3], "type":data[4]}
    response = requests.request("POST", url, data=payload, headers=headers)

    # Show additional info for troubleshooting
    if verbose:
        print "Posted to API : " + str(payload) + "Response - " + str(response.status_code)
        print response.text
    return

try:
    DB_NAME = settings.DB_NAME
    url = settings.URL
    api_key = settings.API_KEY
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

    t = (int(last_idx),)
    c.execute('SELECT * FROM measure WHERE idx>?', t)
    measures = c.fetchall()

except  Exception, e:
    print e
    print "Could read from DB"

for mm in measures:
    postData(api_key,mm)
    time.sleep(2)

try:
    if len(measures)>0: 
        c.execute('UPDATE read_idx SET table_idx = ? WHERE table_name = ?',( mm[0],'measure'))
    conn.commit()
    c.close()
    conn.close()
except  Exception, e:
    print e
    print "Could not close connection to DB"
