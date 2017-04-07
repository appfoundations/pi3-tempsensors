*Python script to read from multiple DS18B20 + 1wire sensors and post data to simple API*
============================================================================================

Background:

I created this script as a simple way to read temperature from multiple 1wire sensors using a Raspberry Pi3 and then send those readings back to a simple web API using http posts. I am using a simple breakout circuit for the pi that contains one terminal block and a 10k resistor to pullup between the 3.3v and data line. This circuit only requires 3 wires to be connect to the Pi and has been tested successfully with over 30 sensors (both the raw component and the waterproof type).

Files:

- getHumidity.py - script to get current humidity (and temp) from DHT11, DHT22 opr DHT2032, uses/requires https://github.com/adafruit/Adafruit_Python_DHT. This script should be scheduled via
- getTemps.py - script to pull current temperature from 1WIRE bus. Can be single or any number or chained/parallel DS18B20 sensors all connected to 1 GPIO pin (4)
- monitorSwitch.py - script to monitor the state of GPIO pins used primary for mangentic door switches but could be any type of switch (e.g. push button, PIR etc)
- settings_template.py - settings file for your api end point (if you want to push data somewhere and a couple of switches for getTemps.py) please copy to 'settings.py' and put your desired settings in there

Making it autorun:

To have this autorun when the pi reboots, i just added a @reboot line to my crontab with a full path to the script, note I have set the Pi to use Wifi, this script will fail if no internet connection is present (if anyone would like to fix that please feel free!)

e.g.
@reboot python /home/pi/pi3-tempsensors/getTemps.py

Acknowledments:

Many thanks to ThePiHut guys for the initial script, ive adapted it to handle multiple sensors and post to an API endpoint (basic http post).

https://thepihut.com/blogs/raspberry-pi-tutorials/18095732-sensors-temperature-with-the-1-wire-interface-and-the-ds18b20



getHumidity.py
getTemps.py
monitorDoors.py