import time
import subprocess
import os
import requests
import settings

# Initialise
def initialise():
  os.system('modprobe w1-gpio')  # Activate GPIO module
  os.system('modprobe w1-therm') # Activate Temperature module
  os.system('clear') # clear screen

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

# post data to api using python requests
def postTemp(probeID,temp):
  headers = {'content-type': 'application/x-www-form-urlencoded'}
  payload = {"key":key,"probeID": probeID,"temp": temp}
  response = requests.request("POST", url, data=payload, headers=headers)
  
  # Show additional info for troubleshooting
  if verbose:
    print "Posted to API : " + str(payload) + "Response - " + str(response.status_code)
    print response.text
  return

# main program loop
def mainLoop():
  while 1:
	  probes=findProbes()
          for probe in probes:
              probeData = readFile(probe)
              probeID = probe.split("/")[4]
              tempdata = probeData.split("\n")[1].split(" ")[9]
              temperature = float(tempdata[2:]) / 1000
              probeNum =  str(probes.index(probe)+1)
              print "Probe " + probeNum + " (id: " + probeID + ") Current Temperature is " + str(temperature) + " C"
              if apipost:
                postTemp(probeID,temperature)
          time.sleep(60)




# define vars
probes = ''

# read settings from settings.py
key = settings.KEY
url = settings.URL
apipost = settings.APIPOST
verbose = settings.VERBOSE

# main program
initialise()

#probes=findProbes()
mainLoop()



