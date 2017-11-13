import time
import threading
import multiprocessing
import RPi.GPIO as GPIO
import serialController as sC
import audioController as aC

call_pin = 6
uno_pin = 7
sim_pin = 11
phone_pin = 12
call_signal = 0
uno_signal = 'l'
sim_signal = 'l'
phone_signal = 'l'
GPIO.setmode(GPIO.BOARD)
GPIO.setup(call_pin, GPIO.IN)       #Make a call
GPIO.setup(uno_pin, GPIO.OUT)       #UNO signal
GPIO.setup(sim_pin, GPIO.OUT)       #SIM signal
GPIO.setup(phone_pin, GPIO.OUT)     #Phone signal

msg_manager = multiprocessing.Manager()
serial_dict = msg_manager.dict()

rate = 0
lng = 116.403963
lat = 39.915119
phone_number = None
try_call = 0

def gpio():
    call_signal = GPIO.input(call_pin)
    if call_signal == 0:
        if phone_number is not None:#press
            serial_dict['SIM_ATD'] = phone_number
            try_call = 0
    if uno_signal == 'h':
        GPIO.output(uno_pin, GPIO.HIGH)
    else:
        GPIO.output(uno_pin, GPIO.LOW)
    if sim_signal == 'h':
        GPIO.output(sim_pin, GPIO.HIGH)
    else:
        GPIO.output(sim_pin, GPIO.LOW)
    if phone_signal == 'h':
        GPIO.output(sim_pin, GPIO.HIGH)
    elif phone_signal == 'm':
        for i in range(3):
            GPIO.output(phone_pin, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(phone_pin, GPIO.LOW)
            time.sleep(0.2)
    else:
        GPIO.output(phone_pin, GPIO.LOW)


def core_function():
    while True:
        for key in serial_dict.keys():
            if key == 'UNO_OK':
                if serial_dict['UNO_OK']:
                    uno_signal = 'h'
                else:
                    uno_signal = 'l'
                del serial_dict['UNO_OK']
            elif key == 'UNO_MSG':
                AT = serial_dict['UNO_MSG'].split(':')
                if AT[0] == 'RATE':
                    rate = float(AT[1])
                elif AT[0] == 'LNG':
                    lng = float(AT[1])
                elif AT[0] == 'LAT':
                    lat = float(AT[1])
                print(serial_dict['UNO_MSG'])
                del serial_dict['UNO_MSG']
            elif key == 'SIM_OK':
                if serial_dict['SIM_OK']:
                    uno_signal = 'h'
                else:
                    uno_signal = 'l'
                del serial_dict['SIM_OK']
            elif key == 'SIM_PHO':
                if serial_dict['SIM_PHO'] == 'Incoming':
                    if serial_dict['SIM_NUM'] == phone_number:
                        serial_dict['SIM_ATA'] = True
                    else:
                        serial_dict['SIM_ATH'] = True
                    time.sleep(0.2)
                elif serial_dict['SIM_PHO'] == 'Fail':
                    if try_call < 5:
                        try_call += 1
                        if phone_number is not None:  # press
                            serial_dict['SIM_ATD'] = phone_number
                    else:
                        try_call = 0
                else:
                    try_call = 0
                del serial_dict['SIM_PHO']
            elif key =='SIM_STA':
                if serial_dict['SIM_STA'] == 'On':
                    phone_signal = 'h'
                elif serial_dict['SIM_STA'] == 'Waiting':
                    phone_signal = 'm'
                else:
                    phone_signal = 'l'



if __name__ == "__main__":
    audioDevice = aC.search_device()
    if audioDevice is None:
        print("[ERROR] Not find USB Audio card.")
    else:
        recordProcess, handleProcess = aC.core(audioDevice)
    serialProcess = multiprocessing.Process(target=sC.core, args={serial_dict})
    serialProcess.start()
    core_function()
