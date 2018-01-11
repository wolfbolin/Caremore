import socket
import struct
import json
import time
import commons


def connect():
    # Socket client
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            print("[INFO] Connecting to server...")
            sock.connect(commons.server_addr)
            break
        except (socket.error, socket.timeout, socket.gaierror, socket.herror) as e:
            print("[ERROR]", e)
            time.sleep(5)
    print("[INFO] Connect to server success")
    return sock


def send_msg(sock, json_msg):
    message = b''
    if 'File' in json_msg.keys():
        # Pack the file
        data_msg = open(commons.cache + json_msg['File'], 'rb').read()
        data_len = struct.pack(commons.byte_order, len(data_msg))
        # Pack the json
        json_msg = json.dumps(json_msg, ensure_ascii=False).encode("utf-8")
        json_len = struct.pack(commons.byte_order, len(json_msg))
        print(json_msg)
        message = json_len + data_len + json_msg + data_msg
    else:
        # There is not File
        data_len = struct.pack(commons.byte_order, 0)
        # Pack the json
        json_msg = json.dumps(json_msg, ensure_ascii=False).encode("utf-8")
        json_len = struct.pack(commons.byte_order, len(json_msg))
        message = json_len + data_len + json_msg
    sock.sendall(message)


if __name__ == "__main__":
    sock = connect()
