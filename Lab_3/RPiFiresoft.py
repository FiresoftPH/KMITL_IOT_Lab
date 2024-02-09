"""
Created by Pattarapark Chutisamoot

This files contains the functions commonly used in Raspberry Pi Projects, it will be used to avoid any repitition of code.
"""

import time
import spidev

def initSPI(spi_number, spi_ce, max_speed_hz):
    spi = spidev.SpiDev()
    spi.open(spi_number, spi_ce)
    spi.max_speed_hz = max_speed_hz
    return spi

# Function to read SPI data from MCP3008 chip (default delay is 0.1)
def readSPIADC(spi_object, adcChannel, printOut = False, delay=0.1):
    raw = spi_object.xfer2([1, (adcChannel<<4 | 0x80), 0])
    data = ((raw[1]&3) << 8) + raw[2]
    if printOut:
        print("RAW ADC Output :" + str(data))
    time.sleep(delay)
    return data