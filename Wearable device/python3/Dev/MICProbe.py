import re
import pyaudio
import wave
import numpy as np
import scipy.signal as signal

print("==============Pre-treatment==============")
RATE = 44100
CHANNELS = 1
FORMAT = pyaudio.paInt16
DEVICE = None
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "recordVoice.wav"
WEAKEN_OUTPUT_FILENAME = "recordVoice-weaken.wav"

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
frames_weak = []
maxVoice = 0
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    audio_data = np.fromstring(data, dtype=np.short)
    for i in range(0,1024):
        maxVoice = max(maxVoice,audio_data[i])
        if(audio_data[i]>1000):
            audio_data[i] = 1000
            print("overflow")
        if (audio_data[i] < -1000):
            audio_data[i] = -1000
            print("overflow")
    frames.append(data)
    frames_weak.append(audio_data)
print(">>>Ending")
print(maxVoice)
stream.stop_stream()
stream.close()
pa.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(pa.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

wf = wave.open(WEAKEN_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(pa.get_sample_size(FORMAT))
wf.setframerate(RATE)
wave_data = np.array(frames_weak).astype(np.short)
wf.writeframes(wave_data.tostring())
wf.close()
