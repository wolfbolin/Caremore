import time
import commons
import threading
import multiprocessing
import RPi.GPIO as GPIO
import audio_service as aS
import serial_service as sS
import network_service as nS


def core_service(serial_dict, sock, sock_lock):
    try_call = 0
    gps_time = 0
    while True:
        call_signal = GPIO.input(commons.call_pin)
        if call_signal == 0:
            print('[INFO] User pass the button')
            try_call = 0
            serial_dict['SIM_ATD'] = True
            GPIO.output(commons.button_pin, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(commons.button_pin, GPIO.LOW)
        if 'SIM_PHO' in serial_dict.keys() and serial_dict['SIM_PHO'] == 'Fail':
            del serial_dict['SIM_PHO']
            if try_call < 5:
                try_call += 1
                serial_dict['SIM_ATD'] = True
            else:
                try_call = 0

        # Set led mode
        if serial_dict['SIM_OK']:
            GPIO.output(commons.sim_pin, GPIO.HIGH)
        else:
            GPIO.output(commons.sim_pin, GPIO.LOW)
        if serial_dict['UNO_OK']:
            GPIO.output(commons.uno_pin, GPIO.HIGH)
        else:
            GPIO.output(commons.uno_pin, GPIO.LOW)
        if serial_dict['SIM_STA'] == 'On':
            GPIO.output(commons.phone_pin, GPIO.HIGH)
        elif serial_dict['SIM_STA'] == 'Close':
            GPIO.output(commons.phone_pin, GPIO.LOW)
        elif serial_dict['SIM_STA'] == 'Waiting':
            for i in range(3):
                GPIO.output(commons.phone_pin, GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(commons.phone_pin, GPIO.LOW)
                time.sleep(0.2)

        if int(time.time()) % 60 == gps_time:
            if gps_time == 0:
                gps_time = 30
            else:
                gps_time = 0
            json_msg = {
                "Action": "GPS",
                "From": "IOT",
                "Lng": str(serial_dict['LNG']/1000000),
                "Lat": str(serial_dict['LAT']/1000000)
            }
            sock_lock.acquire()
            nS.send_msg(sock, json_msg)
            sock_lock.release()


if __name__ == "__main__":
    # Initialization
    # Hard device
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(commons.call_pin, GPIO.IN)  # Make a call
    GPIO.setup(commons.uno_pin, GPIO.OUT)  # UNO signal
    GPIO.setup(commons.sim_pin, GPIO.OUT)  # SIM signal
    GPIO.setup(commons.button_pin, GPIO.OUT)    # Button signal
    GPIO.setup(commons.phone_pin, GPIO.OUT)  # Phone signal
    # audio_device = aS.search_device()  # Try to connect the USB audio card
    # Software
    sock = nS.connect()                 # Try to connect the server
    sock_lock = multiprocessing.Lock()
    msg_manager = multiprocessing.Manager()
    serial_dict = msg_manager.dict()
    serial_dict['RATE'] = 96
    serial_dict['LAT'] = 30527546
    serial_dict['LNG'] = 114356625
    serial_dict['PHONE'] = commons.phone_number
    serial_dict['SIM_STA'] = 'Close'
    serial_dict['SIM_OK'] = False
    serial_dict['UNO_OK'] = False
    # Create the new process
    serialProcess = multiprocessing.Process(target=sS.serial_service, args=(serial_dict,))
    serialProcess.start()
    print("[INFO] Open serial process complete.")
    recordProcess = aS.aduio_service(serial_dict, sock, sock_lock)
    recordProcess.start()
    core_service(serial_dict, sock, sock_lock)
