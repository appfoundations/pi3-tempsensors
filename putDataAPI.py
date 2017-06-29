#!/usr/bin/python
# Copyright (c) 2017 Logicc Systems Ltd.
# Author: Andre Neto
  
import time
import subprocess
import os
import requests
import settings
import sqlite3
import sys

try:
    DB_NAME = settings.DB_NAME
    url = settings.URL
    api_key = settings.API_KEY
    apipost = settings.APIPOST
    verbose = settings.VERBOSE
except:
    print "Could not read settings"
    sys.exit(1)


def postToUrl(key,data):
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    payload = {"key":api_key,"id":data[0],"datecollected": data[1], "probeid": data[2],"temp": data[3], "type":data[4]}
    try:
        response = requests.request("POST", url, data=payload, headers=headers)
    except Exception, e:
        print e
        print __name__ + ": error on url post"

    # Show additional info for troubleshooting
    if verbose:
        print "Posted to API : " + str(payload)
        print "Response - " + str(response.status_code)
        # print response.text
    return response.status_code

def postDBData():
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        t = ('measure',)
        c.execute('SELECT table_idx FROM read_idx WHERE table_name=?',t)
        try :
            last_idx = c.fetchone()[0]
        except :
            last_idx = 0

        t = (int(last_idx),)
        c.execute('SELECT * FROM measure WHERE idx>?', t)
        measures = c.fetchall()
        c.close()
        conn.close()

    except  Exception, e:
        print e
        print __name__ + ": Could not read from DB"
        return

    post = ''
    lastIdx = None
    for mm in measures:
        post = postToUrl(api_key,mm)
        if post == 200 :
            lastIdx = mm[0]
        else :
            break
        time.sleep(1)

    try:
        if (len(measures)>0 and lastIdx is not None): 
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('UPDATE read_idx SET table_idx = ? WHERE table_name = ?',( mm[0],'measure'))
            conn.commit()
            c.close()
            conn.close()
    except  Exception, e:
        print e
        print __name__ + ": Could not close connection to DB"
