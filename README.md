*Python script to read from multiple DS18B20 + 1wire sensors and post data to simple API*
============================================================================================

Background:

I created this script as a simple way to read temperature from multiple 1wire sensors using a Raspberry Pi3 and then send those readings back to a simple web API using http posts. I am using a simple breakout circuit for the pi that contains one terminal block and a 10k resistor to pullup between the 3.3v and data line. This circuit only requires 3 wires to be connect to the Pi and has been tested successfully with over 30 sensors (both the raw component and the waterproof type).

Files:

- getTemps.py - main script, call from shell using `python getTemps.py`
- settings.py - settings file for your api end point and a couple of switches for getTemps.py

Making it autorun:

To have this autorun when the pi reboots, i just added a @reboot line to my crontab with a full path to the script, note I have set the Pi to use Wifi, this script will fail if no internet connection is present (if anyone would like to fix that please feel free!)

e.g.
@reboot python /home/pi/pi3-tempsensors/getTemps.py

Acknowledments:

Many thanks to ThePiHut guys for the initial script, ive adapted it to handle multiple sensors and post to an API endpoint (basic http post).

https://thepihut.com/blogs/raspberry-pi-tutorials/18095732-sensors-temperature-with-the-1-wire-interface-and-the-ds18b20
