import SocketServer
import threading
import commons
from calculateManager import recv_msg


class RequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        sock = self.request
        addr = self.client_address
        user = ""
        print "[INFO] Connect to", addr
        # Open handling and forwardly sending thread for each client
        handling_thread = threading.Thread(target=RequestHandler.handle_message_thread,
                                           args=(sock, addr, user))
        sending_thread = threading.Thread(target=RequestHandler.sending_message_thread,
                                          args=(sock, addr, user))
        handling_thread.start()
        sending_thread.start()
        handling_thread.join()
        sending_thread.join()

    @staticmethod
    def handle_message_thread(sock, addr, user):
        while True:
            try:
                json = recv_msg(sock)
                user = json['From']

            except OSError as e:
                print "[ERROR] OS erroe %s." %e

    @staticmethod
    def sending_message_thread(sock, addr, user):
        while True:
            try:
                recv = ""
                #recv = sock.recv(1024)
            except OSError as e:
                print "[ERROR] OS erroe %s." %e


if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer(('', commons.PORT),RequestHandler)
    print "[INFO] Server started on port %s." %commons.PORT
    server.serve_forever()
