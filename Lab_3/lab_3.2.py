import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

BROKER = "kmitl.ddns.net"
port = 9001

LAMP_PIN = 4
INPUT_TOPIC = "FiresoftHome/LampCmd"
OUTPUT_TOPIC = "FiresoftHome/LampSta"

def on_message(client, user_data, message):
    print("Recieve : " + str(message.payload.decode("utf-8")) + "\n")
    if message.payload.decode("utf-8") == "0":
        client.publish(OUTPUT_TOPIC, "0")
        GPIO.output(LAMP_PIN, False)
    else:
        client.publish(OUTPUT_TOPIC, "1")
        GPIO.output(LAMP_PIN, True)

def on_connect(client, user_data, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print("Connection failed")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LAMP_PIN, GPIO.OUT)
        
client = mqtt.Client(transport="websockets")
client.username_pw_set(username="kmitliot", password="KMITL@iot1234")
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, port)
client.subscribe(INPUT_TOPIC, 0)
client.loop_forever()