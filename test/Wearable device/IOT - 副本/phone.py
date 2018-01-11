import time
import json
import struct
import socket
import commons


def recv_msg(sock):
    try:
        json_len = sock.recv(4)
        json_len = struct.unpack(commons.byte_order, json_len)[0]
        data_len = sock.recv(4)
        data_len = struct.unpack(commons.byte_order, data_len)[0]
        json_msg = sock.recv(json_len)
        data_msg = sock.recv(data_len)
        json_msg = json.loads(json_msg)
        if data_len != 0:
            file_write(json_msg['File'], data_msg)
        return json_msg
    except (socket.error, socket.timeout, socket.gaierror, socket.herror) as e:
        raise


def file_write(filename, data):
    f = open("phone_cache/" + filename, 'wb')
    f.write(data)
    f.close()


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            sock.connect(('127.0.0.1', 8088))
            while True:
                json_msg = recv_msg(sock)
                print("[INFO] Receive message from server")
                print(json_msg)
        except (socket.error, socket.timeout, socket.gaierror, socket.herror) as e:
            print("[ERROR]", e)
            time.sleep(5)
    print("[INFO] Connect to server success")
