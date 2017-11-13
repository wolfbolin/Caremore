# Import modular
import serial

RPiSerial = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)

while True:
    str = input("Input:")
    RPiSerial.write(str.encode())
    print("Response:", RPiSerial.read(1000))

