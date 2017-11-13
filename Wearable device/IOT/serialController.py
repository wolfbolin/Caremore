import time
import serial
import threading


def uno_translator(uno_serial, serial_dict):
    while True:
        if 'UNO_ATI' in serial_dict:
            uno_serial.write(serial_dict['UNO_ATI'].encode("utf-8"))
            del serial_dict['UNO_ATI']
            time.sleep(0.2)
        count = uno_serial.inWaiting()
        if count != 0:
            recv = uno_serial.readline()
            recv = recv.decode()
            # Some code to analysis
            serial_dict['UNO_ATO'] = recv.rstrip()
            # Analysis end


def sim_translator(sim_serial, serial_dict):
    while True:
        if 'SIM_ATD' in serial_dict:
            AT = "ATD" + serial_dict['SIM_Call'] + ";"
            sim_serial.write(AT.encode("utf-8"))
            del serial_dict['SIM_Call']
            time.sleep(0.5)
        if 'SIM_ATH' in serial_dict:
            AT = "ATH"
            sim_serial.write(AT.encode("utf-8"))
            del serial_dict['SIM_ATH']
            time.sleep(0.2)
        if 'SIM_ATA' in serial_dict:
            AT = "ATA"
            sim_serial.write(AT.encode("utf-8"))
            del serial_dict['SIM_ATA']
            time.sleep(0.2)
        if 'SIM_ATI' in serial_dict:
            AT = serial_dict['SIM_ATI']
            sim_serial.write(AT.encode("utf-8"))
            del serial_dict['SIM_ATI']
            time.sleep(0.2)
        count = sim_serial.inWaiting()
        if count != 0:
            recv = sim_serial.readline()
            recv = recv.decode().rstrip()
            # Some code to analysis
            if recv == 'OK':
                continue
            elif recv == 'RING':
                serial_dict['SIM_PHO'] = 'Incoming'
            elif recv == 'NO DIALTONE' or recv == 'NO ANSWER':
                serial_dict['SIM_PHO'] = 'Fail'
            elif recv == 'BUSY' or recv == 'NO CARRIER':
                serial_dict['SIM_PHO'] = 'Close'
            elif recv[0:4] == '+CLCC':
                AT = recv.split(',')
                serial_dict['SIM_NUM'] = AT[5].strip('"')
                if AT[1] == "0":
                    serial_dict['SIM_STA'] = 'On'
                elif AT[1] == "6":
                    serial_dict['SIM_STA'] = 'Close'
                else:
                    serial_dict['SIM_STA'] = 'Waiting'
            elif recv[0:4] == '+CMTI':
                AT = 'AT+CMGD="DEL ALL"'
                sim_serial.write(AT.encode("utf-8"))
                time.sleep(0.2)
            # Analysis end
        

def core(serial_dict):
    sim_serial = serial.Serial("/dev/ttyAMA0", 19200, timeout=1)
    uno_serial = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
    if uno_serial.isOpen():
        serial_dict['UNO_OK'] = True
        uno_thread = threading.Thread(target=uno_translator, args=(uno_serial, serial_dict))
    else:
        serial_dict['UNO_OK'] = False
        uno_thread = None
    if sim_serial.isOpen():
        serial_dict['SIM_OK'] = True
        sim_serial.write("AT+CLCC=1".encode("utf-8"))
        sim_serial.write("AT+CMGF=1".encode("utf-8"))
        sim_thread = threading.Thread(target=sim_translator, args=(sim_serial, serial_dict))
    else:
        serial_dict['SIM_OK'] = False
        sim_thread = None
    try:
        if uno_thread is not None:
            uno_thread.start()
        if sim_thread is not None:
            sim_thread.start()
        while True:
            if uno_thread.isAlive() is False:
                serial_dict['UNO_OK'] = False
                uno_thread.start()
            if sim_thread.isAlive() is False:
                serial_dict['SIM_OK'] = False
                sim_thread.start()
        uno_thread.join()
        sim_thread.join()
    except:
        print(">>>serialController:Something wrong! Can't open thread.")
