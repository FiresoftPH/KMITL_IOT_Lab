"""
Created by Pattarapark Chutisamoot
"""
import RPi.GPIO as GPIO
from RPiFiresoft import initSPI, readSPIADC
# Not needed since already imported in RPiFiresoft
# import spidev
import time
import _thread

# Define GPIO Pins for LEDs and set the pinmodes.
RED_LED_PIN = 26
GREEN_LED_PIN = 21

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)

# Turn off the LEDs
GPIO.output(RED_LED_PIN, False)
GPIO.output(GREEN_LED_PIN, False)

spi = initSPI(spi_number=0, spi_ce=0, max_speed_hz=1000000)
pwm = GPIO.PWM(RED_LED_PIN, 10000)

# Controls the green LED to turn on when it is dark and turn off when it is bright.
def lightSensorGreenLED(value):
    # print(value) # Used when finding the values of the dark room.
    if value > 850:
        GPIO.output(GREEN_LED_PIN, True)
        GPIO.output(RED_LED_PIN, False)
    else:
        GPIO.output(GREEN_LED_PIN, False)
        GPIO.output(RED_LED_PIN, False)

# Controls the Red LED via PWM according to the value of the potentiometer.
def potentiometerRedLED(value):
    # print(value)
    pwm.start(0)
    # 1023 is the max value of the potentiometer (for 10-bit ADC)
    # 100 is the max value of the PWM, so we need to convert the value from
    # the potentiometer to a value between 0 and 100.
    duty_cycle = round(value / 1023 * 100)
    # print(duty_cycle)
    pwm.ChangeDutyCycle(duty_cycle)
    # smooth_dimming(pwm, duty_cycle)
    time.sleep(0.1)
    # pwm.stop()

# Reads the value from the potentiometer and controls the Red LED via PWM.
while True:
    ch_0_value = readSPIADC(spi_object=spi, adcChannel=0)
    _thread.start_new_thread(lightSensorGreenLED, (ch_0_value,))
    ch_1_value = readSPIADC(spi_object=spi, adcChannel=1)
    _thread.start_new_thread(potentiometerRedLED, (ch_1_value,))