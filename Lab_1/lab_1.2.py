"""
Created by Pattarapark Chutisamoot
"""

import RPi.GPIO as GPIO
from time import sleep
import _thread

# Define GPIO Pins for the RGB LED, LED and Button
RED_LED_PIN = 20
GREEN_LED_PIN = 26
RGB_G_PIN = 22
RGB_B_PIN = 27
RGB_R_PIN = 17
BUTTON_PIN = 21

# Setup Pinmode and configuration for the GPIO PIns
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
GPIO.setup(RGB_G_PIN, GPIO.OUT)
GPIO.setup(RGB_B_PIN, GPIO.OUT)
GPIO.setup(RGB_R_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Function use to control the RGB LED to avoid repitition
count = 0
def changeColor(R, G, B):
    global count
    GPIO.output(RGB_R_PIN, R)
    GPIO.output(RGB_G_PIN, G)
    GPIO.output(RGB_B_PIN, B)
    count += 1
    sleep(0.5)

changeColor(True, True, True)

# This main thread controls the Red lED to blink every 1 second.
def mainThread():
    while True:
        GPIO.output(RED_LED_PIN, True)
        sleep(1)
        GPIO.output(RED_LED_PIN, False)
        sleep(1)

# This interupt thread controls the RGB LED to change color when the button is pushed.
def interuptRGB(channel):
    global count
    # RED
    if count == 0:
        changeColor(False, True, True)

    # GREEN
    elif count == 1:
        changeColor(True, False, True)
    
    # BLUE
    elif count == 2:
        changeColor(True, True, False)

    # YELLOW (RED and GREEN)
    elif count == 3:
        changeColor(False, False, True)

    # PURPLE (RED and BLUE)
    elif count == 4:
        changeColor(False, True, False)

    # CYAN (BLUE and GREEN)
    elif count == 5:
        changeColor(True, False, False)

    # WHITE (RED, GREEN and BLUE)
    elif count == 6:
        changeColor(False, False, False)

    # TURN OFF (OPTIONAL not included in the assignment):
    # elif count == 7:
        changeColor(True, True, True)
        count = 0

# This sub thread controls the Green RGB LED to dim for 1 second and 
# then brighten for 1 second. Incremental constant is 10%
# by using PWM. (Pull Width Modulation)
def subThread():
    pwm = GPIO.PWM(GREEN_LED_PIN, 100)
    while True:
        pwm.start(0)
        # By using these for loops, we can control the PWM percentage.
        for i in range(10, 101, 10):
            pwm.ChangeDutyCycle(i)
            # print("Current PWM Percentage", i)
            sleep(1 / 10)
        for i in range(90, -1, -10):
            pwm.ChangeDutyCycle(i)
            # print("Current PWM Percentage", i)
            sleep(1 / 10)
        pwm.stop()

# Start sub thread by using _thread module.
_thread.start_new_thread(subThread, ())
# Attach interupt to the button pin.
GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=interuptRGB, bouncetime=200)
mainThread()