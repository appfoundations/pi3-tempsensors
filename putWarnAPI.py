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


def postWarn(probeid, descr):
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    payload = {"key":api_key,"probeid":probeid,"descr":descr}
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

