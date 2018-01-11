import re
import wave
import time
import commons
import pyaudio


def record_audio(audio_device):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=audio_device,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


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


if __name__ == '__main__':
    print("[INFO] Audio recording.")
    shell = 'arecord -D "plughw:1,0" -t wav -c 1 -f S16_LE -r 48000 -d 5 '
    shell += commons.cache
    shell += time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".wav"
    print(shell)
    # audio_device = search_device()
    # record_audio(audio_device)

