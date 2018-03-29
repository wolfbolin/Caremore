# -*- coding:utf-8 -*-
import json
import time
import random
import socket
import commons
import requests
import threading
import multiprocessing
from flask import Flask,jsonify,send_file, send_from_directory,g
from socket_tools import recv_msg, send_msg
from audio_service import audio_service

refresh_json = {"Action": "Danger", "Message": "No data", "File": "20180329035431.wav", "ID": "20180329035431", "Type": "威胁", "Level": "3", "Heart": "96", "Lng": "112.991970", "Lat": "28.147384"}
info_json = {"Status": "Fail", "Lng": "112.991970", "Lat": "28.147384"}
send_success = False


def IOT_service(stream_push, message_push):
    sock_manager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_manager.bind(('', commons.port_for_IOT))
    sock_manager.listen(10)
    global info_json
    while True:
        print('[INFO] Waiting for IOT connection.')
        sock, addr = sock_manager.accept()
        print('[INFO] Connect to IOT', addr)
        while True:
            try:
                json_msg = recv_msg(sock)
                print('[INFO] Receive message from IOT.', json_msg)
                if json_msg['Action'] == 'GPS':
                    info_json = json_msg
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
                json_msg['Type'] = "诱导类语句"
                json_msg['Level'] = DL_json['Level']
                message_push.send(json_msg)
            elif DL_json['itype'] == "2":
                json_msg['Action'] = "Danger"
                json_msg['Type'] = "威胁恐吓类"
                json_msg['Level'] = DL_json['Level']
                message_push.send(json_msg)
            elif DL_json['itype'] == "3":
                json_msg['Action'] = "Danger"
                json_msg['Type'] = "暴力语言类"
                json_msg['Level'] = DL_json['Level']
                message_push.send(json_msg)
            else:
                continue


def phone_service(message_pop):
    global refresh_json
    global send_success
    while True:
        while send_success:
            time.sleep(0.1)
        json_msg = message_pop.recv()
        send_success = True
        refresh_json = json_msg


http_app = Flask("caremore")


@http_app.route('/status')
def status():
    return jsonify({'Action': 'status', 'Message': "server running"})


@http_app.route('/confirm')
def confirm():
    global send_success
    send_success = False
    return jsonify({'Action': 'confirm', 'Message': "success"})


@http_app.route('/refresh')
def refresh():
    return jsonify(refresh_json)


@http_app.route('/info')
def info():
    return jsonify(info_json)


@http_app.route('/download/<file>')
def download(file):
    return send_from_directory(commons.cache, file, as_attachment=True)


@http_app.route('/player/<file>')
def player(file):
    return send_from_directory(commons.cache, file)


if __name__ == '__main__':
    (stream_push, stream_pop) = multiprocessing.Pipe()
    (audio_in, audio_out) = multiprocessing.Pipe()
    (message_push, message_pop) = multiprocessing.Pipe()

    process_IOT = multiprocessing.Process(target=IOT_service, args=(stream_push, message_push))
    process_audio = multiprocessing.Process(target=audio_service, args=(audio_out,))
    process_stream = multiprocessing.Process(target=stream_service, args=(stream_pop, audio_in, message_push))
    # process_phone = multiprocessing.Process(target=phone_service, args=(message_pop,))

    process_phone = threading.Thread(target=phone_service, args=(message_pop,))

    process_IOT.start()
    process_audio.start()
    process_stream.start()
    # process_phone.start()
    process_phone.start()

    http_app.run(host='0.0.0.0')

    process_IOT.join()
    process_audio.join()
    process_stream.join()
    process_phone.join()





