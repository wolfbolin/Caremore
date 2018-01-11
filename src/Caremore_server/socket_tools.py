import json
import socket
import struct
import commons


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
    except socket.error:
        print('[ERROR] Receive message error.Socket error')
        raise


def send_msg(sock, json_msg):
    print('[INFO] Danger:', json_msg)
    if json_msg['Action'] == 'Message':
        # Pack the file
        data_msg = file_read(json_msg['File'])
        data_len = struct.pack(commons.byte_order, len(data_msg))
        # Pack the json
        json_msg = json.dumps(json_msg, ensure_ascii=False).encode("utf-8")
        json_len = struct.pack(commons.byte_order, len(json_msg))
        message = json_len + data_len + json_msg + data_msg
    else:
        # There is not File
        data_len = struct.pack(commons.byte_order, 0)
        # Pack the json
        json_msg = json.dumps(json_msg, ensure_ascii=False).encode("utf-8")
        json_len = struct.pack(commons.byte_order, len(json_msg))
        message = json_len + data_len + json_msg
    try:
        sock.sendall(message)
    except socket.error:
        print('[ERROR] Send message error.Socket error')
        raise


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
