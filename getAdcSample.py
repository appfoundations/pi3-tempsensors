# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import settings
import sqlite3

try:
    CLK = settings.CLK
    MISO = settings.MISO
    CS = settings.CS
    MOSI = settings.MOSI
    DB_NAME = settings.DB_NAME
except:
    print "Could not read settings"
    sys.exit(1)

mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
# SPI_PORT   = 0
# SPI_DEVICE = 0
# mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


# print('Reading MCP3008 values, press Ctrl-C to quit...')
value = '{0:0.1f}'.format(mcp.read_adc(1) * 3.3 / 1024 * 20)
print value

try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    t = ('PI_KEY',)
    c.execute('SELECT value FROM params WHERE name=?', t)
    serial = c.fetchone()[0]
    db_entry = (str('MCP3008[0]')+'@'+str(serial),value,'current')
    c.execute("INSERT INTO measure (time,probeId,measure, type) VALUES (CURRENT_TIMESTAMP,?,?,?)", db_entry)
    conn.commit()
    c.close()
    conn.close()
except  Exception, e:
    print e
    print "Could not save to DB"