import sys
from urllib.request import urlopen

# first_name = input("Enter your first name: ")
# last_name = input("Enter your last name: ")

def checkAttendance(first_name, last_name):
    URL = "http://kmitl.ddns.net/iot/cie/Pattarapark/insert.php?name=" + first_name + "_" + last_name
    response = urlopen(URL)

    print("Insert ", first_name, last_name, " into the table")
    if response.read().decode("utf-8") == "1":
        print("Insertion successful")

    else:
        print("Insertion failed")