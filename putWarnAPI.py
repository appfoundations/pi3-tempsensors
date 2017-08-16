#!/usr/bin/python
# Copyright (c) 2017 Logicc Systems Ltd.
# Author: Andre Neto
  
import requests
import settings
import sys

try:
    DB_NAME = settings.DB_NAME
    url = settings.URL_WARN
    api_key = settings.API_KEY
    apipost = settings.APIPOST
    verbose = settings.VERBOSE
except:
    print "Could not read settings"
    sys.exit(1)


def postWarn(probeids, descr):
    if verbose:
        print "Post warn request to " + url
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    payload = {"key":api_key,"descr":descr}

    print str(probeids)

    for i,id in enumerate(probeids):
        payload["probeid["+str(i)+"]"] = id

    print str(payload)

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

