import time
import socket
import commons
import datapack
import multiprocessing
from audio_stream import aduio_service


def core_service(audio_poster):
    DL_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            print("[INFO] Try to connect the server.")
            DL_server.connect(commons.send_addr)
            break
        except (socket.error, socket.timeout, socket.gaierror, socket.herror) as e:
            print("[ERROR]", e)
            time.sleep(5)
    sock_IOT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_IOT.bind(commons.recv_addr)
    sock_IOT.listen(5)
    while True:
        print('waiting for connection')
        recv_sock, recv_addr = sock_IOT.accept()
        print('connect from ', recv_addr)
        while True:
            try:
                json_msg = datapack.recv_msg(recv_sock)
            except BaseException as e:
                print("[ERROR]", e)
                recv_sock.close()
                break
            print("[INFO] Receive a message.Begin to handle.", end="")
            print(json_msg)
            if json_msg['Action'] == 'Audio':
                audio_poster.send(json_msg)
                json_msg = audio_poster.recv()
                if json_msg['Action'] == 'Fail':
                    continue
            try:
                datapack.send_msg(DL_server, json_msg)
            except BaseException as e:
                print("[ERROR]", e)
                DL_server.close()
                try:
                    DL_server.connect(commons.send_addr)
                except (socket.error, socket.timeout, socket.gaierror, socket.herror) as e:
                    print("[ERROR]", e)
                    time.sleep(5)
        recv_sock.close()


if __name__ == "__main__":
    (audio_poster, audio_handler) = multiprocessing.Pipe()
    poster = multiprocessing.Process(target=core_service, args=(audio_poster,))
    handler = multiprocessing.Process(target=aduio_service, args=(audio_handler,))
    poster.start()
    handler.start()
    poster.join()
    handler.join()

