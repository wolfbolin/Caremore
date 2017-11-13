import json
import struct
import commons


def recv_msg(sock):
    json_len = sock.recv(4)
    json_len = struct.unpack(commons.BYTEORDER, json_len)[0]
    data_len = sock.recv(4)
    data_len = struct.unpack(commons.BYTEORDER, data_len)[0]
    json_msg = sock.recv(json_len)
    data_msg = sock.recv(data_len)
    json_msg = json.loads(json_msg)
    if data_len != 0:
        file_write(json_msg['File'], data_msg)
    return json_msg


def send_msg(sock, json_msg):
    message = b''
    json_len = struct.pack(commons.BYTEORDER, len(json_msg))
    if 'File' in json_msg and json_msg['File'] != '':
        data_msg = file_read(json_msg['File'])
        data_len = struct.pack(commons.BYTEORDER, len(data_msg))
        message = json_len + data_len + json.dumps(json_msg) + data_msg
    else:
        data_len = struct.pack(commons.BYTEORDER, len(message))
        message = json_len + data_len + json.dumps(json_msg)
    sock.sendall(message)


def file_write(filename, data):
    f = open(commons.CACHE+"\\"+filename, 'wb')
    f.write(data)
    f.close()


def file_read(filename):
    f = open(commons.CACHE + "\\" + filename, 'rb')
    return f.read()

