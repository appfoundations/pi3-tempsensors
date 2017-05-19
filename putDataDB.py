#!/usr/bin/python
# Copyright (c) 2017 Logicc Systems Ltd.
# Author: Andre Neto

import sys
import settings
from time import sleep
import sqlite3

try:
    verbose = settings.VERBOSE
    DB_NAME = settings.DB_NAME
except Exception, e:
    print __name__ + ": Could not read settings"
    print e
    sys.exit(1)


def postData(data):
    try:
        conn = sqlite3.connect(DB_NAME,15)
    except  Exception, e:
        print e
        print "Could not open to DB"
        sys.exit(1)

    try:
        conn.executemany("INSERT INTO measure (time,probeId,measure, type) VALUES (datetime('now', 'localtime'),?,?,?)", data)
        conn.commit()
    except  Exception, e:
        print e
        print "Could not post to DB"
        sys.exit(1)

    try:
        conn.close()
    except Exception, e:
        print e
        print "Could not close DB connection"


def cleanData():
    try:
        conn = sqlite3.connect(DB_NAME,15)
    except  Exception, e:
        print e
        print "Could not open to DB"
        sys.exit(1)

    try:
        c = conn.cursor()
        t = ('measure',)
        c.execute('SELECT table_idx FROM read_idx WHERE table_name=?',t)
        try :
            last_idx = c.fetchone()[0]-500
        except :
            last_idx = 0

        t = (int(last_idx),)
        c.execute('DELETE FROM measure WHERE idx<?', t)
        conn.commit()
        conn.execute("VACUUM")

    except  Exception, e:
        print e
        print "Could not DELETE/VACCUM DB"

    try:
        conn.close()
    except Exception, e:
        print e
        print "Could not close DB connection"