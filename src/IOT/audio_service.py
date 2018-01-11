import os
import re
import time
import wave
import commons
import multiprocessing
import network_service as nS


def aduio_service(serial_dict, sock, sock_lock):
    recordProcess = multiprocessing.Process(target=record_audio, args=(serial_dict, sock, sock_lock))
    if __name__ == '__main__':
        recordProcess.start()
    else:
        return recordProcess


def record_audio(serial_dict, sock, sock_lock):
    while True:
        print("[INFO] Audio recording.")
        file_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".wav"
        file_path = commons.cache + file_name
        shell = 'arecord -D "plughw:1,0" -t wav -c 1 -f S16_LE -r 48000 -d ' + str(commons.second) + ' '
        shell += file_path
        print(os.popen(shell))
        time.sleep(commons.second + 0.1)
        print("[INFO] Recording end.")

        # Send audio to server
        print("[INFO] Send audio to server.")
        json_msg = {
            "Action": "Audio",
            "ID": file_name[0:14],
            "From": "IOT",
            "Lng": str(serial_dict['LNG'] / 1000000),
            "Lat": str(serial_dict['LAT'] / 1000000),
            "Heart": str(serial_dict['RATE']),
            "File": file_name
        }

        sock_lock.acquire()
        nS.send_msg(sock, json_msg)
        sock_lock.release()
        os.remove(file_path)
