"""
Created by Pattarapark Chutisamoot
"""

# Import the libraries.
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from time import sleep
import _thread

# Setup the broker and the port alongside the GPIO pins.
BROKER = "kmitl.ddns.net"
port = 9001

RED_RGB_PIN = 22
GREEN_RGB_PIN = 27
BLUE_RGB_PIN = 17

# RED_RGB_PIN = 17
# GREEN_RGB_PIN = 22
# BLUE_RGB_PIN = 27

# The topic for the input and output.
INPUT_TOPIC = "FiresoftHome/RGBCmd"
RED_OUTPUT_TOPIC = "FiresoftHome/RGBRedStatus"
GREEN_OUTPUT_TOPIC = "FiresoftHome/RGBGreenStatus"
BLUE_OUTPUT_TOPIC = "FiresoftHome/RGBBlueStatus"

# This thread checks the status of the RGB LED and publish the status to the broker.
def checkStatus():
    while True:
        if GPIO.input(RED_RGB_PIN) == False:
            client.publish(RED_OUTPUT_TOPIC, 1)
        else:
            client.publish(RED_OUTPUT_TOPIC, 0)
        
        if GPIO.input(GREEN_RGB_PIN) == False:
            client.publish(GREEN_OUTPUT_TOPIC, 1)
        else:
            client.publish(GREEN_OUTPUT_TOPIC, 0)
        
        if GPIO.input(BLUE_RGB_PIN) == False:
            client.publish(BLUE_OUTPUT_TOPIC, 1)
        else:
            client.publish(BLUE_OUTPUT_TOPIC, 0)
        
        sleep(0.25)

# This function is called when a message is recieved from the broker.
def on_message(client, user_data, message):
    decoded_message = str(message.payload.decode("utf-8"))
    print("Recieve : " + str(decoded_message) + "\n")
    if decoded_message == "greenon":
        GPIO.output(GREEN_RGB_PIN, False)
    elif decoded_message == "blueon":
        GPIO.output(BLUE_RGB_PIN, False)
    elif decoded_message == "redon":
        GPIO.output(RED_RGB_PIN, False)
    elif decoded_message == "greenoff":
        GPIO.output(GREEN_RGB_PIN, True)
    elif decoded_message == "blueoff":
        GPIO.output(BLUE_RGB_PIN, True)
    elif decoded_message == "redoff":          
        GPIO.output(RED_RGB_PIN, True)

# This function is called when the client connects to the broker.
def on_connect(client, user_data, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print("Connection failed")

# Setup the GPIO pins.
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(GREEN_RGB_PIN, GPIO.OUT)
GPIO.setup(BLUE_RGB_PIN, GPIO.OUT)
GPIO.setup(RED_RGB_PIN, GPIO.OUT)

# Turn off the RGB LED.
GPIO.output(GREEN_RGB_PIN, True)
GPIO.output(BLUE_RGB_PIN, True)
GPIO.output(RED_RGB_PIN, True)
# Start the thread to check the status of the RGB LED.
_thread.start_new_thread(checkStatus, ())

# Setup the client and connect to the broker.
client = mqtt.Client(transport="websockets")
client.username_pw_set(username="kmitliot", password="KMITL@iot1234")
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, port)
client.subscribe(INPUT_TOPIC, 0)
client.loop_forever()