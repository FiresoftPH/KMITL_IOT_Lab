import RPi.GPIO as GPIO
import MFRC522
import signal
import time
continue_reading = True

# Capture SIGINT for cleanup when the script is aborted.
def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Capture SIGINT for cleanup when the script is aborted.
def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Add white spaces to the strings for writing to the RFID card.
def addWhiteSpace(string):
    while len(string) < 16:
        string += " "
    return string

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

GPIO.setmode(GPIO.BOARD)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print("Welcome to the MFRC522 data write")
print("Press Ctrl-C to stop.")

while continue_reading:

    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    if status == MIFAREReader.MI_OK:
        print("Card detected")

    (status, uid) = MIFAREReader.MFRC522_Anticoll()
    
    if status == MIFAREReader.MI_OK:
        print("Card read UID: ", uid[0], ":", uid[1], ":", uid[2], ":", uid[3])
        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        MIFAREReader.MFRC522_SelectTag(uid)
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        if status == MIFAREReader.MI_OK:
            first_name = addWhiteSpace("Pattarapark")
            last_name = addWhiteSpace("Chutisamoot")
            data_1 = bytes(first_name, "ascii")
            data_2 = bytes(last_name, "ascii")

            print("Sector 8 & 9 looked like this: ")

            name_1 = MIFAREReader.MFRC522_Readdata(8)
            name_2 = MIFAREReader.MFRC522_Readdata(9)

            name_1 = "".join(map(chr, name_1))
            name_2 = "".join(map(chr, name_2))

            print(name_1 + " " + name_2 + "\n")

            print("Write data to sector 8 & 9: ")

            MIFAREReader.MFRC522_Write(8, data_1)
            MIFAREReader.MFRC522_Write(9, data_2)
            
            print("Now look like this: ")

            name_1 = MIFAREReader.MFRC522_Readdata(8)
            name_2 = MIFAREReader.MFRC522_Readdata(9)
            
            name_1 = "".join(map(chr, name_1))
            name_2 = "".join(map(chr, name_2))
            print(name_1 + " " + name_2 + "\n")

            MIFAREReader.MFRC522_StopCrypto1()
            continue_reading = False
        else:
            print("Authentication error")