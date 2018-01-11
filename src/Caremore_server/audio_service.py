import os
import commons
from aip import AipSpeech
from pydub import AudioSegment
from audio_package.speech_segmentation import multi_segmentation


def audio_service(audio_out):
    aipSpeech = AipSpeech(commons.APP_ID, commons.API_KEY, commons.SECRET_KEY)
    residue_audio = None
    while True:
        # Set handle object name and path
        json_msg = audio_out.recv()
        file_name = json_msg['File']
        file_path = commons.cache + file_name

        # Mix the residue audio and handle object
        print("[INFO] Begin to handle wav ", file_name)
        if residue_audio is not None:
            handle_audio = AudioSegment.from_file(file_path, format="wav", frame_rate=commons.rate)
            audio = residue_audio + handle_audio
            audio.export(file_path, format='wav')

        # Some negative optimization
        # if audio.dBFS < 0:
        #     audio += abs(audio.dBFS)
        # noise_reduction(file_path)

        # To calculate how to segment the audio by BIC
        try:
            seg_result = multi_segmentation(file_path, commons.rate)
        except BaseException as e:
            print("[ERROR] Because of segmentation", e)
            json_msg['Action'] = 'Fail'
            audio_out.send(json_msg)
            continue
        if len(seg_result) < 2:
            print("[INFO] Discard this audio")
            json_msg['Action'] = 'Fail'
            audio_out.send(json_msg)
            continue

        # Open the mix audio and ready to segment it.
        audio = AudioSegment.from_file(file_path, format="wav", frame_rate=commons.rate)
        a = int(seg_result[0] * 1000) - 100
        b = int(seg_result[len(seg_result) - 2] * 1000) + 100
        if a >= b:
            residue_audio = None
            print("[INFO] Discard this audio")
            json_msg['Action'] = 'Fail'
            audio_out.send(json_msg)
            continue
        if a <= 0:
            a = 1
        if b >= len(audio):
            b = len(audio)-1
        mix_audio = audio[a: b]
        # Retain some audio for next handle.
        # This step is older to ensure we will not less too much information.
        residue_audio = audio[int(seg_result[len(seg_result) - 2] * 1000) - 100:]

        # Export a audio file for aipSpeech
        aip_audio = mix_audio.set_frame_rate(16000)
        aip_audio.export(file_path + ".aip.wav", format="wav")

        mix_audio = mix_audio.set_channels(2)
        mix_audio.export(file_path, format="wav")

        # Push task into thread poll
        # Identifying audio by AipSpeech
        print("[INFO] Handle audio is already complete.Start identifying audio.")
        aip_result = aipSpeech.asr(open(file_path + ".aip.wav", 'rb').read(), 'wav', 16000, {'lan': 'zh', })
        # Identifying complete.Clean cache
        os.remove(file_path + ".aip.wav")
        # Identifying result
        if 'err_msg' not in aip_result:
            json_msg['Action'] = 'Fail'
            audio_out.send(json_msg)
            continue
        if aip_result['err_msg'] == "success.":
            print("[INFO] Result:", aip_result['result'][0])
        else:
            print("[ERROR] Error code:", aip_result['err_msg'])

        # To ensure the information is useful
        if aip_result['err_msg'] != "success." or len(aip_result['result'][0].encode("utf-8")) < 4:
            print("Identifying audio Fail.")
            json_msg['Action'] = 'Fail'
            audio_out.send(json_msg)
            continue
        print("[INFO] Identifying audio complete.Begin to send message to stream")
        json_msg['Action'] = 'Message'
        json_msg['Message'] = aip_result['result'][0]
        audio_out.send(json_msg)
