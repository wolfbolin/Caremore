# -*- coding:utf-8 -*-
import time
import commons
import multiprocessing
import socket
import random
from calculateManager import recv_msg, send_msg
from Caremore_DP import Caremore_DL


def socket_IOT(phone_in, server_in):
    addr = ('', commons.stream_port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(addr)
    sock.listen(1)
    caremore_model = Caremore_DL()
    while True:
        print('waiting for connection')
        stream_sock, phone_addr = sock.accept()
        print('connect from ', addr)
        while True:
            try:
                # str = stream_sock.recv(1024)
                # print str.decode()
                json_msg = recv_msg(stream_sock)
                print "[INFO] Receive message from IOT.", json_msg
                if json_msg['Action'] == "GPS":
                    phone_in.send(json_msg)
                elif json_msg['Action'] == "Message":
                    server_in.send(json_msg)
            except BaseException as e:
                print "[ERROR] ", e
                stream_sock.close()
                break
        stream_sock.close()
    sock.close()


def socket_DL(server_out, phone_in):
    addr = ('', commons.DL_port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(addr)
    sock.listen(1)
    while True:
        print('waiting for connection')
        server_sock, server_addr = sock.accept()
        print('connect from ', addr)
        while True:
            json_msg = server_out.recv()
            server_sock.sendall(json_msg['Message'].encode('utf8'))
            itype = server_sock.recv(1024).decode('utf8')
            if json_msg['Heart'] > 140:
                json_msg['Heart'] = 128
            if itype == "1":
                json_msg['Action'] = "Danger"
                json_msg['Type'] = "1"
                json_msg['Level'] = random.choice([2, 3, 4])
                phone_in.send(json_msg)
            elif itype == "2":
                json_msg['Action'] = "Danger"
                json_msg['Type'] = "2"
                json_msg['Level'] = random.choice([2, 3, 4])
                phone_in.send(json_msg)
            elif itype == "3":
                json_msg['Action'] = "Danger"
                json_msg['Type'] = "3"
                json_msg['Level'] = random.choice([2, 3, 4])
                phone_in.send(json_msg)


def socket_phone(phone_out):
    addr = ('', commons.phone_port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(addr)
    sock.listen(1)
    while True:
        print('waiting for connection')
        phone_sock, phone_addr = sock.accept()
        print('connect from ', addr)
        while True:
            try:
                json_msg = phone_out.recv()
                send_msg(phone_sock, json_msg)
                print "[INFO] Send message to phone.", json_msg
            except BaseException as e:
                print "[ERROR] From Send to phone", e
                phone_sock.close()
                break
        phone_sock.close()
    sock.close()


if __name__ == "__main__":
    (phone_in, phone_out) = multiprocessing.Pipe()
    (server_in, server_out) = multiprocessing.Pipe()
    conn_IOT = multiprocessing.Process(target=socket_IOT, args=(phone_in, server_in))
    conn_DL = multiprocessing.Process(target=socket_DL, args=(server_out, phone_in))
    conn_phone = multiprocessing.Process(target=socket_phone, args=(phone_out,))
    conn_IOT.start()
    conn_DL.start()
    conn_phone.start()

    # for i in range(0, 10):
    #     text = raw_input("text:").decode("utf8")
    #     print type(text)
    #     json_msg = {
    #         "Action": "Danger",
    #         "ID": "20171117085557",
    #         "From": "IOT",
    #         "Lat": "28.139109",
    #         "Lng": "112.989077",
    #         "Heart": 89,
    #         "Type": "3",
    #         "Level": 4,
    #         "Message": text,
    #         "File": "20171117085557.wav"
    #     }
    #     print json_msg
    #     phone_in.send(json_msg)
    #     time.sleep(1)

    conn_IOT.join()
    conn_DL.join()
    conn_phone.join()
