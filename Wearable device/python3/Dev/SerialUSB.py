import serial
import time

RPiSerial = serial.Serial("/dev/ttyUSB0", 19200, timeout=1)

while True:
    str = input("Input:")
    RPiSerial.write(str.encode("utf8"))
    time.sleep(2)
    count = RPiSerial.inWaiting()
    if count != 0:
        print("Response")
        print("=======================")
        while count != 0:
            recv = RPiSerial.readline()
            print(">>>", end = '')
            print(recv.decode("gbk"))
            time.sleep(0.5)
            count = RPiSerial.inWaiting()
        print("=======================")
    RPiSerial.flushInput()
