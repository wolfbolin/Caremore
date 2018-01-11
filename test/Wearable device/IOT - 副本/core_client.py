import time
import threading
import multiprocessing
import RPi.GPIO as GPIO

import commons
import serial_tools as sT
import audio_tools as aT
import network_tools as nT


def core_service(serial_dict, sock_lock, sock):
    try_call = 0
    while True:
        call_signal = GPIO.input(commons.call_pin)
        if call_signal == 0:
            try_call = 0
            serial_dict['SIM_ATD'] = True
        if serial_dict['SIM_PHO'] == 'Fail':
            del serial_dict['SIM_PHO']
            if try_call < 5:
                try_call += 1
                serial_dict['SIM_ATD'] = True
            else:
                try_call = 0
        elif serial_dict['SIM_STA'] == 'On':
            GPIO.output(commons.phone_pin, GPIO.HIGH)
        elif serial_dict['SIM_STA'] == 'Close':
            GPIO.output(commons.phone_pin, GPIO.LOW)
        elif serial_dict['SIM_STA'] == 'Waiting':
            for i in range(3):
                GPIO.output(commons.phone_pin, GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(commons.phone_pin, GPIO.LOW)
                time.sleep(0.2)
        elif serial_dict['SIM_OK']:
            GPIO.output(commons.sim_pin, GPIO.HIGH)
        elif ~serial_dict['SIM_OK']:
            GPIO.output(commons.sim_pin, GPIO.LOW)
        elif serial_dict['UNO_OK']:
            GPIO.output(commons.uno_pin, GPIO.HIGH)
        elif ~serial_dict['UNO_OK']:
            GPIO.output(commons.uno_pin, GPIO.LOW)
        if int(time.time()) % 10 == 0:
            json_msg = {
                "Action": "GPS",
                "From": "IOT",
                "Lng": str(serial_dict['LNG']/1000000),
                "Lat": str(serial_dict['LAT']/1000000)
            }
            sock_lock.acquire()
            nT.send_msg(sock, json_msg)
            sock_lock.release()


if __name__ == "__main__":
    # Initialization
    # Hard device
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(commons.call_pin, GPIO.IN)  # Make a call
    GPIO.setup(commons.uno_pin, GPIO.OUT)  # UNO signal
    GPIO.setup(commons.sim_pin, GPIO.OUT)  # SIM signal
    GPIO.setup(commons.phone_pin, GPIO.OUT)  # Phone signal
    audio_device = aT.search_device()  # Try to connect the USB audio card
    # Software
    sock = nT.connect()                 # Try to connect the server
    sock_lock = threading.Lock()
    msg_manager = multiprocessing.Manager()
    serial_dict = msg_manager.dict()
    serial_dict['RATE'] = 0
    serial_dict['LNG'] = 116403963
    serial_dict['LAT'] = 39915119
    serial_dict['PHONE'] = commons.phone_number
    serial_dict['SOCKET'] = None
    serial_dict['SIM_STA'] = 'Close'
    serial_dict['SIM_OK'] = False
    serial_dict['UNO_OK'] = False
    # Create the new process
    serialProcess = multiprocessing.Process(target=st.serial_service(), args=(serial_dict,))
    serialProcess.start()
    print("[INFO] Open serial process complete.")
    time.sleep(10)
    if audio_device is not None:
        recordProcess, handleProcess = sT.aduio_service(audio_device, serial_dict, sock, sock_lock)
        recordProcess.start()
        handleProcess.start()
        print("[INFO] Open audio process complete.")
    else:
        print("[ERROR] Can't open audio process.")
    core_service(serial_dict, sock_lock, sock)

    # while True:
    #     json_msg = {
    #         "Action": "GPS",
    #         "From": "IOT",
    #         "Lng": serial_dict['LNG'],
    #         "Lat": serial_dict['LAT'],
    #     }
    #     sock_lock.acquire()
    #     nT.send_msg(sock, json_msg)
    #     sock_lock.release()
    #     time.sleep(5)
