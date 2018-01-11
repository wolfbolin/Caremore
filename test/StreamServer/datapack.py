import os
import json
import struct
import commons
import socket


def recv_msg(sock):
    try:
        json_len = recv_all(sock, 4)
        json_len = struct.unpack(commons.byte_order, json_len)[0]
        data_len = recv_all(sock, 4)
        data_len = struct.unpack(commons.byte_order, data_len)[0]
        json_msg = recv_all(sock, json_len)
        json_msg = json_msg.decode("utf-8")
        json_msg = json.loads(json_msg)
        if data_len != 0:
            data_msg = recv_all(sock, data_len)
            file_write(json_msg['File'], data_msg)
        return json_msg
    except (socket.error, socket.timeout, socket.gaierror, socket.herror) as e:
        raise


def send_msg(sock, json_msg):
    message = b''
    if json_msg['Action'] == 'Message':
        # Pack the file
        file_path = commons.cache + json_msg['File']
        data_msg = file_read(json_msg['File'])
        data_len = struct.pack(commons.byte_order, len(data_msg))
        # Pack the json
        json_msg = json.dumps(json_msg, ensure_ascii=False).encode("utf-8")
        json_len = struct.pack(commons.byte_order, len(json_msg))
        message = json_len + data_len + json_msg + data_msg
        # Clean cache
        # os.remove(file_path)
    else:
        # There is not File
        data_len = struct.pack(commons.byte_order, 0)
        # Pack the json
        json_msg = json.dumps(json_msg, ensure_ascii=False).encode("utf-8")
        json_len = struct.pack(commons.byte_order, len(json_msg))
        message = json_len + data_len + json_msg
    sock.sendall(message)


def file_write(filename, data):
    f = open(commons.cache + filename, 'wb')
    f.write(data)
    f.close()


def file_read(filename):
    f = open(commons.cache + filename, 'rb')
    return f.read()

def recv_all(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data
