import socket
import struct
import json
import commons


def connect():
    # Socket client
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(commons.server_addr)
    except:
        sock = None
    return sock


def send_msg(sock, json_msg):
    message = b''
    json_msg = json.dumps(json_msg)
    json_len = struct.pack(commons.byte_order, len(json_msg))
    if 'File' in json_msg and json_msg['File'] != '':
        data_msg = open("./cache/" + json_msg['File']).read()
        data_len = struct.pack(commons.byte_order, len(data_msg))
        message = json_len + data_len + json_msg + data_msg
    else:
        data_len = struct.pack(commons.byte_order, len(message))
        message = json_len + data_len + json.dumps(json_msg)
    sock.sendall(message)


if __name__ == "__main__":
    sock = connect()
    if sock is None:
        print("[ERROR] Socket open failed.")
    else:
        print("[INFO] Socket open success.")
