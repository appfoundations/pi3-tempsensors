# pi3-tempsensors

Pythong script to read from multiple DS18B20 + 1wire sensors and post data to web hook


Files
getTemps.py - main script, call from shell using `python getTemps.py`
settings.py - settings file for your api end point and a couple of switches for getTemps.py

To have this autorun when the pi reboots, i just added a @reboot line to my crontab with a full path to the script

e.g.
@reboot python /home/pi/

Acknowledments:

Thanks to these guys for the initial script, ive since adapted it to handle multiple sensors and post to an API endpoint (basic http post).
https://thepihut.com/blogs/raspberry-pi-tutorials/18095732-sensors-temperature-with-the-1-wire-interface-and-the-ds18b20
