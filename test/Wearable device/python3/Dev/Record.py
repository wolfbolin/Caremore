import re
import pyaudio
import wave

print("==============Pre-treatment==============")
RATE = 44100
CHANNELS = 1
FORMAT = pyaudio.paInt16
DEVICE = None
CHUNK = 1024
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"

pa = pyaudio.PyAudio()

print("==============Audio device information==============")
for i in range(0, pa.get_device_count()):
    print(pa.get_device_info_by_index(i))
for i in range(0, pa.get_device_count()):
    deviceName = pa.get_device_info_by_index(i)['name']
    deviceInputChannels = pa.get_device_info_by_index(i)['maxInputChannels']
    isUSBDevice = re.search(".USB.", str(deviceName))   #regex
    isUSBDevice = isUSBDevice or re.search("USB.", str(deviceName)) #regex
    if isUSBDevice and deviceInputChannels != 0:
        print(">>>The index of USB Audio Device is ", i)
        print(">>>", pa.get_device_info_by_index(i))
        DEVICE = i
        break
if DEVICE is None:
    print(">>>The USB sound card is missing")
    exit()

isSupported = pa.is_format_supported(rate=RATE,
                                     input_device=DEVICE,
                                     input_channels=CHANNELS,
                                     input_format=FORMAT)
if isSupported:
    print(">>>ACCEPT:The device support recording.")
else:
    print(">>>ERROR:The device does not support recording.")
    exit()

print("==============Pre-treatment complete==============")


stream = pa.open(rate=RATE,
                 channels=CHANNELS,
                 format=FORMAT,
                 input=True,
                 input_device_index=DEVICE,
                 frames_per_buffer=CHUNK)
print(">>>Recording")
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print(">>>Ending")
stream.stop_stream()
stream.close()
pa.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(pa.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
