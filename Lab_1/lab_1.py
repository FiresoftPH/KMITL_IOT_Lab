import RPi.GPIO as GPIO
from time import sleep

# Define GPIO Pins for the RGB LED and Button
R_PIN = 22
G_PIN = 27
B_PIN = 17
BUTTON_PIN = 25

# Setup Pinmode and configuration for the GPIO PIns
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(R_PIN, GPIO.OUT)
GPIO.setup(G_PIN, GPIO.OUT)
GPIO.setup(B_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Function use to control the RGB LED to avoid repitition
count = 0
def changeColor(R, G, B):
    global count
    GPIO.output(R_PIN, R)
    GPIO.output(G_PIN, G)
    GPIO.output(B_PIN, B)
    count += 1
    sleep(0.25)

changeColor(True, True, True)

count = 0
while True:
    if GPIO.input(BUTTON_PIN) == True:
        print("Button was pushed!")
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
            count = 0