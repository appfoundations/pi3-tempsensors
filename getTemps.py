import time
import subprocess
import os

# Clear screen
os.system('clear')

# Set up find command
findCMD = 'find /sys/devices/ -name "w1_slave"'
out = subprocess.Popen(findCMD,shell=True,stdin=subprocess.PIPE, 
                        stdout=subprocess.PIPE,stderr=subprocess.PIPE)
# Get standard out and error
(stdout, stderr) = out.communicate()
 
# Save found files to list
filelist = stdout.decode().split()


#for probe in filelist:
#    print "Probe found in : %s" % probe
#quit()

while 1:
	for probe in filelist:
	    #tempfile = open("/sys/bus/w1/devices/28-00000620bd7a/w1_slave")
	    tempfile = open(probe)	    
	    thetext = tempfile.read()
	    tempfile.close()
	    probeid = probe.split("/")[4]
	    tempdata = thetext.split("\n")[1].split(" ")[9]
	    temperature = float(tempdata[2:])
	    temperature = temperature / 1000
	    print "Probe " + str(filelist.index(probe)+1) + " (id: " + probeid + ") Current Temperature is " + str(temperature) + "C"
	time.sleep(5)
	os.system('clear')
