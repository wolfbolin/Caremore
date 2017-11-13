# ATManager.py
"""
Description:
Use Raspberry Pi to control the SIM800H Modular by AT instructions.
2017/10/14
"""

# Import modular
import serial
import RPi.GPIO as GPIO

# Declare variable
GSMLoop = True
RPiSerial = None
SIM800H = 23
GSMSignal = 8
Conversation = 7
Emergency = 21
PhoneNumber = ""

# Initialization
GPIO.setmode(GPIO.BOARD)
GPIO.setup(SIM800H, GPIO.OUT)
GPIO.setup(GSMSignal, GPIO.OUT)
GPIO.setup(Conversation, GPIO.OUT)
GPIO.setup(Emergency, GPIO.IN)
GPIO.output(SIM800H, GPIO.LOW)
GPIO.output(GSMSignal, GPIO.OUT)
GPIO.output(Conversation, GPIO.OUT)

# Control the conversation
def Connecting():
    while True:
        msg = RPiSerial.read(1000)
        if msg[0:5] == "+CLCC:":
            return

# Receive message function
def Loop():
    while GSMLoop:
        ButtonValue = GPIO.input(Emergency)
        if ButtonValue == True:
            # Check the net work
            # Make a call
            RPiSerial.write(("ATD", PhoneNumber, "；\r\n").encode())
            Connecting()

# Connect the SIM800H
RPiSerial = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)  # Use the serial on Raspberry Pi
RPiSerial.open()
print("Open SIM800H success")
print("Device name:", RPiSerial.name)
print("Device part:", RPiSerial.port)
GPIO.output(SIM800H, GPIO.HIGH)

# Try to send "AT"
RPiSerial.write(("AT\r\n").encode())
print(RPiSerial.read(1000))

# Wait for the network
GPIO.output(GSMSignal, GPIO.HIGH)

# Open the echo?

# Set the setting
RPiSerial.write(("AT+CLCC=1\r\n").encode())

#Wait for setting number
while PhoneNumber == "":
    continue

Loop()
