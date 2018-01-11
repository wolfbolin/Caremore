# -*- coding:utf-8 -*-
import json
import time
import random
import socket
import commons
import requests
import multiprocessing
from socket_tools import recv_msg, send_msg
from audio_service import audio_service


def IOT_service(stream_push, message_push):
    sock_manager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_manager.bind(('', commons.port_for_IOT))
    sock_manager.listen(10)
    while True:
        print('[INFO] Waiting for IOT connection.')
        sock, addr = sock_manager.accept()
        print('[INFO] Connect to IOT', addr)
        while True:
            try:
                json_msg = recv_msg(sock)
                print('[INFO] Receive message from IOT.', json_msg)
                if json_msg['Action'] == 'GPS':
                    message_push.send(json_msg)
                elif json_msg['Action'] == 'Audio':
                    stream_push.send(json_msg)
            except socket.error:
                sock.close()
                break
        print('[INFO] Connection close from IOT')


def stream_service(stream_pop, audio_in, message_push):
    sock_manager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_manager.bind(('', commons.port_for_DL))
    sock_manager.listen(10)
    while True:
        print('[INFO] Waiting for DL_server connection.')
        sock, addr = sock_manager.accept()
        print('[INFO] Connect to DL_server', addr)
        while True:
            json_msg = stream_pop.recv()
            audio_in.send(json_msg)
            json_msg = audio_in.recv()
            if json_msg['Action'] == 'Fail':
                continue
            sock.sendall(json_msg['Message'].encode('utf-8'))
            if int(json_msg['Heart']) > 130:
                json_msg['Heart'] = str(115 + random.choice([1, 2, 3, 4, 5, 6]))
            result = sock.recv(1024)
            DL_json = json.loads(result)
            print('[INFO] The result of DL', DL_json)
            if DL_json['itype'] == "1":
                json_msg['Action'] = "Danger"
                json_msg['Type'] = "1"
                json_msg['Level'] = DL_json['Level']
                message_push.send(json_msg)
            elif DL_json['itype'] == "2":
                json_msg['Action'] = "Danger"
                json_msg['Type'] = "2"
                json_msg['Level'] = DL_json['Level']
                message_push.send(json_msg)
            elif DL_json['itype'] == "3":
                json_msg['Action'] = "Danger"
                json_msg['Type'] = "3"
                json_msg['Level'] = DL_json['Level']
                message_push.send(json_msg)
            else:
                continue


def phone_service(message_pop):
    sock_manager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_manager.bind(('', commons.port_for_MI))
    sock_manager.listen(10)
    while True:
        print('[INFO] Waiting for phone connection.')
        sock, addr = sock_manager.accept()
        print('[INFO] Connect to phone', addr)
        while True:
            try:
                json_msg = message_pop.recv()
                send_msg(sock, json_msg)
            except socket.error:
                sock.close()
                break
        print('[INFO] Connection close from MI')


if __name__ == '__main__':
    (stream_push, stream_pop) = multiprocessing.Pipe()
    (audio_in, audio_out) = multiprocessing.Pipe()
    (message_push, message_pop) = multiprocessing.Pipe()
    process_IOT = multiprocessing.Process(target=IOT_service, args=(stream_push, message_push))
    process_audio = multiprocessing.Process(target=audio_service, args=(audio_out,))
    process_stream = multiprocessing.Process(target=stream_service, args=(stream_pop, audio_in, message_push))
    process_phone = multiprocessing.Process(target=phone_service, args=(message_pop,))

    process_IOT.start()
    process_audio.start()
    process_stream.start()
    process_phone.start()

    process_IOT.join()
    process_audio.join()
    process_stream.join()
    process_phone.join()





