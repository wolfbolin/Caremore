import re
import os
from aip import AipSpeech
import time
import pyaudio
import wave
import commons
import multiprocessing
from pydub import AudioSegment
from audio_package.noiseReduction import noise_reduction
from audio_package.speech_segmentation import multi_segmentation as multi_seg

pa = pyaudio.PyAudio()


def search_device():
    audio_decvice = None
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
            audio_decvice = i
            break
    if audio_decvice is None:
        print("[ERROR] The USB sound card is missing")
        return None

    isSupported = pa.is_format_supported(rate=commons.RATE,
                                         input_device=audio_decvice,
                                         input_channels=commons.CHANNELS,
                                         input_format=commons.FORMAT)
    if isSupported:
        print("[INFO] The device support recording.")
        return audio_decvice
    else:
        print("[INFO] The device does not support recording.")
        return None


def core(audio_decvice):
    (input_pipe, output_pipe) = multiprocessing.Pipe()
    recordProcess = multiprocessing.Process(target=record_audio, args=(input_pipe, audio_decvice))
    handleProcess = multiprocessing.Process(target=handle_audio, args=(output_pipe,))
    if __name__ == '__main__':
        recordProcess.start()
        handleProcess.start()
        recordProcess.join()
        handleProcess.join()
    else:
        return recordProcess, handleProcess


def record_audio(input_pipe, audio_decvice):
    stream = pa.open(rate=commons.RATE,
                     channels=commons.CHANNELS,
                     format=commons.FORMAT,
                     input=True,
                     input_device_index=audio_decvice,
                     frames_per_buffer=commons.CHUNK)
    print("[INFO] Aduio device open success.Begin to record.")
    while True:
        print("[INFO] Audio recording.")
        frames = []
        for i in range(0, int(commons.RATE / commons.CHUNK * commons.RECORD_SECONDS)):
            data = stream.read(commons.CHUNK)
            frames.append(data)
        print("[INFO] Recording end.")

        # stream.stop_stream()
        # stream.close()
        # pa.terminate()
        file_name = time.strftime("%Y%m%d%H%M%S", time.localtime())+".wav"
        file_path = commons.CACHE+file_name
        wf = wave.open(file_path, 'wb')
        wf.setnchannels(commons.CHANNELS)
        wf.setsampwidth(pa.get_sample_size(commons.FORMAT))
        wf.setframerate(commons.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        input_pipe.send(file_name)


def handle_audio(output_pipe):
    aipSpeech = AipSpeech(commons.APP_ID, commons.API_KEY, commons.SECRET_KEY)
    residue_audio = None
    while True:
        file_name = output_pipe.recv()
        file_path = commons.CACHE + file_name
        print("[INFO] Begin to handle wav ", file_name)
        if residue_audio is not None:
            handle_audio = AudioSegment.from_file(file_path, format="wav", frame_rate=commons.RATE)
            audio = residue_audio + handle_audio
            audio.export(file_path, format='wav')
        # if audio.dBFS < 0:
        #     audio += abs(audio.dBFS)
        # noise_reduction(file_path)
        seg_result = multi_seg(file_path, commons.RATE)
        #print(seg_result)
        audio = AudioSegment.from_file(file_path, format="wav", frame_rate=commons.RATE)
        #audio.export(file_path+"-a.wav", format="wav")

        mix_audio = audio[int(seg_result[0]*1000)-100: int(seg_result[len(seg_result)-2]*1000)+100]
        mix_audio.export(file_path, format="wav")

        aip_audio = mix_audio.set_frame_rate(16000)
        aip_audio.export(file_path+".aip.wav", format="wav")

        residue_audio = audio[int(seg_result[len(seg_result)-2]*1000)-100:]
        #residue_audio.export(file_path + "-r.wav", format="wav")

        print("[INFO] Handle audio is already complete.Start identifying audio.")
        aip_result = aipSpeech.asr(open(file_path+".aip.wav", 'rb').read(), 'wav', 16000, {'lan': 'zh', })
        if 'err_msg' not in aip_result:
            continue
        if aip_result['err_msg'] == "success.":
            print("[INFO] ", aip_result['result'])
        else:
            print("[ERROR] Error code:", aip_result['err_msg'])



if __name__ == '__main__':
    device = search_device()
    core(device)
    # file_path = "cache/20171113042426.wav"
    # seg_result = multi_seg(file_path, commons.RATE)
    # print(seg_result)
    # audio = AudioSegment.from_file(file_path, format="wav", frame_rate=commons.RATE)
    # mix_audio = audio[int(seg_result[0] * 1000) - 100: int(seg_result[len(seg_result) - 2] * 1000) + 100]
    # mix_audio = mix_audio.set_frame_rate(16000)
    # mix_audio.export(file_path, format="wav")
