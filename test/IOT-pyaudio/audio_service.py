import os
import re
import time
import wave
import commons
import pyaudio
import multiprocessing
import network_service as nS


def search_device():
    pa = pyaudio.PyAudio()
    audio_device = None
    # for i in range(0, pa.get_device_count()):
    #     print(pa.get_device_info_by_index(i))
    for i in range(0, pa.get_device_count()):
        deviceName = pa.get_device_info_by_index(i)['name']
        deviceInputChannels = pa.get_device_info_by_index(i)['maxInputChannels']
        isUSBDevice = re.search(".USB.", str(deviceName))   #regex
        isUSBDevice = isUSBDevice or re.search("USB.", str(deviceName)) #regex
        if isUSBDevice and deviceInputChannels != 0:
            print("[INFO] The index of USB Audio Device is ", i)
            print("[INFO] Device's information: ", pa.get_device_info_by_index(i))
            audio_device = i
            break
    if audio_device is None:
        print("[ERROR] The USB sound card is missing")
        return None

    isSupported = pa.is_format_supported(rate=commons.rate,
                                         input_device=audio_device,
                                         input_channels=commons.channels,
                                         input_format=commons.format)
    if isSupported:
        print("[INFO] The device support recording.")
        return audio_device
    else:
        print("[INFO] The device does not support recording.")
        return None


def aduio_service(audio_device, serial_dict, sock, sock_lock):
    recordProcess = multiprocessing.Process(target=record_audio, args=(audio_device, serial_dict, sock, sock_lock))
    if __name__ == '__main__':
        recordProcess.start()
    else:
        return recordProcess


def record_audio(audio_device, serial_dict, sock, sock_lock):
    pa = pyaudio.PyAudio()
    stream = pa.open(rate=commons.rate,
                     channels=commons.channels,
                     format=commons.format,
                     input=True,
                     input_device_index=audio_device,
                     frames_per_buffer=commons.chunk)
    print("[INFO] Aduio device open success.Begin to record.")
    while True:
        print("[INFO] Audio recording.")
        file_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".wav"
        file_path = commons.cache + file_name
        shell = 'arecord -D "plughw:1,0" -t wav -c 1 -f S16_LE -r 48000 -d 5 '
        shell += file_path
        print(os.popen(shell))
        # frames = []
        # for i in range(0, int(commons.rate / commons.chunk * commons.rec_seconds)):
        #     data = stream.read(commons.chunk, exception_on_overflow=False)
        #     frames.append(data)
        print("[INFO] Recording end.")

        # stream.stop_stream()
        # stream.close()
        # pa.terminate()
        # wf = wave.open(file_path, 'wb')
        # wf.setnchannels(commons.channels)
        # wf.setsampwidth(pa.get_sample_size(commons.format))
        # wf.setframerate(commons.rate)
        # wf.writeframes(b''.join(frames))
        # wf.close()

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
