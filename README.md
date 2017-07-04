TruckyPI - Mobile sensor logging for cars, trucks and anything else that moves!
================================================================================

Background:

I created this script as a simple way to read temperature from multiple 1wire sensors using a Raspberry Pi3 and then send those readings back to a simple web API using http posts. I am using a simple breakout circuit for the pi that contains one terminal block and a 10k resistor to pullup between the 3.3v and data line. This circuit only requires 3 wires to be connect to the Pi and has been tested successfully with over 30 sensors (both the raw component and the waterproof type).

Since I started, we have since added support for a range of sensors including humidty, door switches and current sensors.

Files:

- getHumidity.py - script to get current humidity (and temp) from DHT11, DHT22 opr DHT2032, uses/requires https://github.com/adafruit/Adafruit_Python_DHT. This script should be scheduled via
- getTemps.py - script to pull current temperature from 1-WIRE bus. Can be single or any number or chained/parallel DS18B20 sensors all connected to 1 GPIO pin (4)
- getSwitch.py - script to read the state of GPIO pins used primary for mangentic door switches but could be any type of switch (e.g. push button, PIR etc)
- getAdc.py - script to interface a MCP3008 adc used to use analog sensors like a Current Sensor, uses/requires Adafruit_MCP3008

- putDataDB.py - module with functions to save collected data in local sqlitedb and sanitize it, uses/requires sqlite3
- putDataAPI.py - module with functions to post collected data to a configured API end point
- putWarnAPI.py - module with function to post a warning message to a configured API end point
- setSiren.py - module with function to play an audio file as warning
- setWarning.py - module with function to evaluate data collected and determine the warning status

- master.py - script master to process the data collection, save, post to API and evaluate warning status
- runDoorsDetect.py - script to monitor the state of GPIO pins used primary for mangentic door switches but could be any type of switch (e.g. push button, PIR etc)

- settings_template.py - settings file for your api end point (if you want to push data somewhere and a couple of switches for getTemps.py) please copy to 'settings.py' and put your desired settings in there
- crontab.sample - crontab configuration to make it autorun
- getLimitsAPI.py - script to read from configured API the sensors limits value

Making it autorun:

To make it autorun please use the crontab.sample example.
master.py collects a single sample of each sensor, should be called repeatedly.
runDoorsDetect.py needs to be running to detect switches status changes 

e.g. 
*/5 * * * * cd /home/pi/pi3-tempsensors-master; python master.py >> logs/master.log &
* * * * * cd /home/pi/pi3-tempsensors-master; ps -ef|grep -v grep|grep runDoorsDetect.py || python runDoorsDetect.py &

Acknowledments:

Many thanks to ThePiHut guys for the initial script, ive adapted it to handle multiple sensors and post to an API endpoint (basic http post).

https://thepihut.com/blogs/raspberry-pi-tutorials/18095732-sensors-temperature-with-the-1-wire-interface-and-the-ds18b20

Also thanks to Tony DiCola for the "Simple example of reading the MCP3008 analog input channels and printing"

https://github.com/adafruit/Adafruit_Python_MCP3008/blob/master/examples/simpletest.py



getHumidity.py
getTemps.py
monitorDoors.py
