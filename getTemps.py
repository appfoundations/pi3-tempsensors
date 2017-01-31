import time
import subprocess
import os
import requests

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

# post data to web hook (simple http post + params)
def postTemp(key,probeID,temperature):
  hdr = {'Content-Type': 'application/json'}
  payload = {"key": key,"probeID": probeID,"temperature": temperature}
  r = requests.post(postURL,params=payload)
  print "Posting to API..."
  print "Response - " + str(r.status_code)
  print r.text
  return

# main program loop
def mainLoop():
  while 1:
          for probe in probes:
              probeData = readFile(probe)
              probeID = probe.split("/")[4]
              tempdata = probeData.split("\n")[1].split(" ")[9]
              temperature = float(tempdata[2:]) / 1000
              probeNum =  str(probes.index(probe)+1)
              print "Probe " + probeNum + " (id: " + probeID + ") Current Temperature is " + str(temperature) + " C"
              if apiPost:
                postTemp(key,probeID,temperature)
          time.sleep(5)
          os.system('clear')

# define vars
probes = ''
key='[api_key]'
postURL='http://api_endpoint]'
apiPost = True # change to false to disable api posting

# main program
initialise()
probes=findProbes()
mainLoop()

