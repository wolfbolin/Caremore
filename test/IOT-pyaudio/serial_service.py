import time
import serial
import threading


def serial_service(serial_dict):
    # Connect to uno board and sim board
    sim_serial = serial.Serial("/dev/ttyAMA0", 19200, timeout=1)
    uno_serial = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)

    # Check the connection
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
        sim_serial.write("AT+CHFA=1".encode("utf-8"))
        sim_serial.write("ATM6".encode("utf-8"))
        sim_serial.write("ATL6".encode("utf-8"))
        sim_thread = threading.Thread(target=sim_translator, args=(sim_serial, serial_dict))
    else:
        serial_dict['SIM_OK'] = False
        sim_thread = None

    # Create thread to begin send and receive message
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


def uno_translator(uno_serial, serial_dict):
    while True:
        # Send message to UNO board
        if 'UNO_GPS' in serial_dict.keys():
            AT = "GPS"
            uno_serial.write(AT.encode("utf-8"))
            del serial_dict['UNO_GPS']
            time.sleep(0.2)

        # Receive message from UNO board
        count = uno_serial.inWaiting()
        if count != 0:
            recv = uno_serial.readline()
            recv = recv.decode().rstrip()
            # Some code to analysis
            # This code can handle:
            # RATE:59
            # LNG:116403963
            # LAT:39915119
            AT = recv.split(':')
            if len(AT) != 2 or len(AT[1]) == 0:
                continue
            serial_dict[AT[0]] = int(AT[1])


def sim_translator(sim_serial, serial_dict):
    while True:
        # Make a call
        if 'SIM_ATD' in serial_dict.keys():
            AT = "ATD" + serial_dict['PHONE'] + ";"
            sim_serial.write(AT.encode("utf-8"))
            del serial_dict['SIM_ATD']
            time.sleep(0.5)

        # Begin to receive AT
        count = sim_serial.inWaiting()
        if count != 0:
            recv = sim_serial.readline()
            recv = recv.decode().rstrip()
            # Some code to analysis
            if recv == 'OK':
                continue
            elif recv == 'RING':
                # Phone in
                serial_dict['SIM_PHO'] = 'Incoming'
            elif recv == 'NO DIALTONE' or recv == 'NO ANSWER':
                # Phone out and no answer
                serial_dict['SIM_PHO'] = 'Fail'
            elif recv == 'BUSY' or recv == 'NO CARRIER':
                # Phone close
                serial_dict['SIM_PHO'] = 'Close'
            elif recv[0:4] == '+CLCC':
                # Connect status update
                AT = recv.split(',')
                # To analysis the phone come from
                if AT[5].strip('"') == serial_dict['PHONE']:
                    # Receive call from target.
                    AT = "ATA"
                    sim_serial.write(AT.encode("utf-8"))
                    time.sleep(0.2)
                else:
                    # Receive call from stranger.
                    AT = "ATH"
                    sim_serial.write(AT.encode("utf-8"))
                    time.sleep(0.2)
                # To set led light status
                if AT[1] == "0":
                    serial_dict['SIM_STA'] = 'On'
                elif AT[1] == "6":
                    serial_dict['SIM_STA'] = 'Close'
                else:
                    serial_dict['SIM_STA'] = 'Waiting'
            elif recv[0:4] == '+CMTI':
                # Receive message and delete.
                AT = 'AT+CMGD="DEL ALL"'
                sim_serial.write(AT.encode("utf-8"))
                time.sleep(0.2)
            # Analysis end
