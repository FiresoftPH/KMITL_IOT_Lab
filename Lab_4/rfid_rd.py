import RPi.GPIO as GPIO
import time
import signal
import MFRC522
from insert_sql import checkAttendance

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted.
def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

GPIO.setmode(GPIO.BOARD)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print("Welcome to the MFRC522 data read")
print("Press Ctrl-C to stop.")

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # IF a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected")

    # Get the UID of the card
    (status, uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        # Print UID
        print("Card read UID: ", uid[0], ":", uid[1], ":", uid[2], ":", uid[3])

        # This is the default key for authentication
        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            data_1 = MIFAREReader.MFRC522_Readdata(8)
            data_2 = MIFAREReader.MFRC522_Readdata(9)
            first_name = "".join(map(chr, data_1))
            last_name = "".join(map(chr, data_2))
            first_name = first_name.strip()
            last_name = last_name.strip()
            print(first_name + " " + first_name)
            checkAttendance(first_name, last_name)
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print("Authentication error")

        time.sleep(1)
