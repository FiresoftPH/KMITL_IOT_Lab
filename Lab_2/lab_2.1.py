import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0) #spi 0, ce0
spi.max_speed_hz = 1000000

def readSPIADC(adcChannel):
    raw = spi.xfer2([1, (adcChannel<<4 | 0x80), 0])
    data = ((raw[1]&3) << 8) + raw[2]
    print("RAW ADC Output :" + str(data))
    time.sleep(1)
    return data

while True:
    digital_output = readSPIADC(adcChannel=0)
    r2_voltage = (digital_output * 3.3) / 1024
    print("Voltage on R2", r2_voltage)
    current = (3.3 - r2_voltage) / 10000
    r2_value = r2_voltage / current
    print("R2 Value", r2_value)