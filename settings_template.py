# settings for getTemps.py

# getTemps script switches
APIPOST = True # change to enable/disable api posting
VERBOSE = True # change to enable/disable verbose output
LOOP  = False # change to false you just want one reading then exit
DELAY = 10 # number of seconds between readings (if running in loop mode)

# API Settings
URL = 'your api endpoint url'
API_KEY = 'your api key'
PI_KEY = 'your pi serial'

# DB Settings
DB_NAME = "database.db" # DB name for measures and params
SQL_FILE_NAME = "db_init.sql" # sql name to DB init

# DHT Info
DHT_V = 11      # DHT version '11': Adafruit_DHT.DHT11, '22': Adafruit_DHT.DHT22, '2302': Adafruit_DHT.AM2302 
DHT_PINS = [17,27]

# CT / ADC Info
ADC_CHANNELS = [0,1]

# Software SPI configuration - MCP3008 ADC:
CLK  = 6
MISO = 13
MOSI = 19
CS   = 26

# Door sensors 
DOOR_PINS = [22,5]
