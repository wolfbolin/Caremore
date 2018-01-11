import os
import time
import socket
from sqlalchemy import Column, String, Boolean, Text, TIMESTAMP, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from predefined_text import text,TEXT,DEVICE
from commons import recv_msg,send_msg,get_time
from config import load_config
from time import ctime
import datetime
import msgpack
import threading
import SocketServer

CONFIG = load_config()
DIVICES = {}
LOGGED_IN_USERS = {}
DB_SESSION_LOCK = {}
ORMBaseModel = declarative_base()
db_engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'
                          .format(CONFIG.DB['user'], CONFIG.DB['password'],
                                  CONFIG.DB['host'], CONFIG.DB['port'],
                                  CONFIG.DB['database']),
                          encoding='utf-8',
                          pool_size=50
                          )
DBSession = sessionmaker(bind=db_engine)

class Message(ORMBaseModel):
    __tablename__ = 'caremore_messages'
    message_id = Column(String(130), primary_key=True)
    type = Column(String(10), nullable=False)
    time = Column(String(255), nullable=False)
    sender = Column(String(40), ForeignKey('ctk_users.username'), nullable=False)
    receiver = Column(String(40), ForeignKey('ctk_users.username'), nullable=False)
    message = Column(Text)
    last_send_time = Column(TIMESTAMP)

    def __repr__(self):
        return "<Message `{}`, last_send_time `{}`>".format(self.message_id, self.last_send_time)

class Attachment(ORMBaseModel):
    __tablename__ = 'ctk_attachments'
    message_id = Column(String(130), ForeignKey('ctk_messages.message_id'), primary_key=True)
    filename = Column(String(255), nullable=False)

    def __repr__(self):
        return "<Attachment `{}` filename=`{}`>".format(self.message_id, self.filename)

# Class      : RemoveOfflineUserThread
# Description: Remove offline users from LOGGED_IN_USERS every 30 seconds
class RemoveOfflineUserThread(threading.Thread):
    def run(self):
        while True:
            logged_in_users_copy = LOGGED_IN_USERS.copy()
            for (k, v) in logged_in_users_copy.items():
                if get_time() - v["time"] > 60:
                    LOGGED_IN_USERS.pop(k)
            time.sleep(30)

class RequestHandler(SocketServer.BaseRequestHandler):
    @staticmethod
    def action_user_login(db_session,device=None):
        if device:
            if device in DEVICE:
                return TEXT["successfully-login"]
            else:
                return TEXT["incorrect-device"]
        else:
            return TEXT["no-device-name"]

    @staticmethod
    def action_send_message(db_session,parameters,username=None):
        # Receiver not exists
        message = {'type': parameters['type'], 'time': parameters['time'], 'receiver': parameters['receiver'],
                   'sender': username, "message_id": ctime()}
        # Message with same id in rare situations
        if db_session.query(Message).filter(Message.message_id == message["message_id"]).first():
            return text("duplicated_message", message["message_id"])

        if parameters["type"] == "text":
            message["message"] = parameters["message"]
            # Save message to database
            db_session.add(Message(message_id=message["message_id"],
                                   type=message["type"],
                                   time=message["time"],
                                   sender=message["sender"],
                                   receiver=message["receiver"],
                                   message=message["message"]))
            db_session.commit()

            return text("message_sent", message["message_id"])
        else:
            # Save file to local
            with open(os.path.join(os.getcwd(), "attachments/{}".format(message["message_id"])), 'wb') as f:
                f.write(parameters["data"])

            # Save message to database
            db_session.add(Message(message_id=message["message_id"],
                                   type=message["type"],
                                   time=message["time"],
                                   sender=message["sender"],
                                   receiver=message["receiver"]))
            db_session.add(Attachment(message_id=message["message_id"],
                                      filename=parameters["filename"]))
            db_session.commit()

            return text("message_sent", message["message_id"])

    @staticmethod
    def forwardly_sending_message_thread(sock, db_session, current_user):
        while True:
            if current_user:
                break
            time.sleep(1)
        time.sleep(10)
        flag_to_quit = False
        while True:
            # If logged in and have message to send
            if current_user:
                DB_SESSION_LOCK[current_user[0]].acquire()
                messages = db_session.query(Message).all()
                DB_SESSION_LOCK[current_user[0]].release()
                for each_message in messages:
                    if not each_message.last_send_time \
                            or datetime.datetime.now() - each_message.last_send_time > datetime.timedelta(seconds=10):
                        # Send message
                        msg_to_send = {
                            "action": "receive-message",
                            "message_id": each_message.message_id,
                            "type": each_message.type,
                            "sender": each_message.sender,
                            "time": each_message.time,
                        }
                        if each_message.type == "text":
                            msg_to_send["message"] = each_message.message
                        else:
                            DB_SESSION_LOCK[current_user[0]].acquire()
                            attachment = db_session.query(Attachment) \
                                .filter(Attachment.message_id == each_message.message_id).first()
                            DB_SESSION_LOCK[current_user[0]].release()
                            msg_to_send["filename"] = attachment.filename
                            with open(os.path.join(os.getcwd(),
                                                    "attachments/{}".format(each_message.message_id)), "rb"
                                    ) as f:
                                msg_to_send["data"] = f.read()

                        try:
                                send_msg(sock, msgpack.dumps(msg_to_send, use_bin_type=True))
                                print("[INFO]Send message %s" % each_message)
                        except socket.error:
                            # Client closed connection
                            flag_to_quit = True
                            break

                        #Update last_send_time of message
                        DB_SESSION_LOCK[current_user[0]].acquire()
                        db_session.query(Message) \
                                .filter(Message.message_id == each_message.message_id) \
                                .update({"last_send_time": datetime.datetime.now()})
                        db_session.commit()
                        DB_SESSION_LOCK[current_user[0]].release()
            if flag_to_quit:
                break
            time.sleep(0.5)

    @staticmethod
    def action_message_received(db_session, parameters, device=None):
        if "message_id" not in parameters:
            return TEXT['incomplete_parameters']

        message = db_session.query(Message).filter(Message.message_id == parameters["message_id"]).first()
        if message.receiver == device:
            # Delete message from database
            db_session.delete(message)
            db_session.commit()

            if message.type != "text":
                # delete attachment from server
                os.remove(os.path.join(os.getcwd(), "attachments/{}".format(message.message_id)))

    @staticmethod
    def do_action(db_session, action, parameters, device=None):
            if CONFIG.DEBUG:
                print("do_action device%s" % device)
            actions = {
                "user-login": RequestHandler.action_user_login,
                "send-message": RequestHandler.action_send_message,
                "message-received": RequestHandler.action_message_received,
            }
            if action not in actions:
                return TEXT["no_such_action"]

            if device:
                DB_SESSION_LOCK[device].acquire()
                msg_to_return = actions[action](db_session, parameters, device=device)
                DB_SESSION_LOCK[device].release()
                return msg_to_return
            elif action == "user-login":
                msg_to_return = actions[action](db_session, parameters)
                return msg_to_return
            else:
                return text("not_login")

    @staticmethod
    def handle_user_request_thread(sock, db_session, current_device):
        while True:
            try:
                recv = recv_msg(sock)
                if recv:
                    accept_data = msgpack.loads(recv, encoding='utf-8')
                    if len(accept_data) > 50:
                        print("[INFO][%s]Accepted data %s...%s" % (len(accept_data),
                                                                    accept_data[0:50],
                                                                    accept_data[-50:-1]))
                    else:
                        print("[INFO][%s]Accepted data %s." % (len(accept_data),
                                                                   accept_data))

                    if "parameters" not in accept_data:
                        send_data = TEXT['incomplete_parameters']

                    # If Bye-bye
                    if accept_data["action"] == "Bye-bye":
                        if current_device:
                            DIVICES.pop(current_device[0])
                        break

                    if current_device:
                        send_data = RequestHandler.do_action(db_session, accept_data["action"],
                                                                accept_data, username=current_device[0])
                    else:
                        send_data = RequestHandler.do_action(db_session, accept_data["action"],
                                                                 accept_data)

                    if send_data:
                        send_msg(sock, msgpack.dumps(send_data, use_bin_type=True))
                        if len(msgpack.dumps(send_data, use_bin_type=True)) > 500:
                            print("send: [%s]%s..." % (len(msgpack.dumps(send_data, use_bin_type=True)[0:50]),
                                                        msgpack.dumps(send_data, use_bin_type=True)[0:50]))
                        else:
                            print("send: [%s]%s" % (len(msgpack.dumps(send_data, use_bin_type=True)),
                                                    msgpack.dumps(send_data, use_bin_type=True)))

                    # if successfully log in, save username to variable username
                    if send_data \
                            and "description" in send_data.keys() \
                            and send_data["description"] == "Login successfully":
                        current_device.append(accept_data["device"])
                        DB_SESSION_LOCK[current_device[0]] = threading.Lock()
                        print("[INFO]User {} logged in.".format(current_device[0]))

            except msgpack.exceptions.UnpackValueError:
                # Client closed connection
                print("[INFO]Client closed the connection(msgpack.exceptions.UnpackValueError).")
                break
            except msgpack.exceptions.ExtraData:
                # Not a msgpack file
                print("[EXCEPTION]Not a msgpack file(msgpack.exceptions.ExtraData)")
                break
            except OSError as e:
                print("[ERROR]OS ERROR %s." % e)
                break

    def handle(self):
        db_session = DBSession()
        socket = self.request
        address = self.client_address
        ssl_sock = socket
        print("[INFO]{} connected.".format(address))
        print("  ")
        current_user = []

        # Open handling and forwardly sending thread for each client
        handling_thread = threading.Thread(target=RequestHandler.handle_user_request_thread,
                                               args=(ssl_sock, db_session, current_user))
        sending_thread = threading.Thread(target=RequestHandler.forwardly_sending_message_thread,
                                              args=(ssl_sock, db_session, current_user))
        handling_thread.start()
        sending_thread.start()
        handling_thread.join()
        sending_thread.join()
        # After joining two threads(client log out)
        print("[INFO]Socket close.")
        ssl_sock.close()
        db_session.close()

if __name__ == '__main__':
    # Start TCP server
    server = SocketServer.ThreadingTCPServer((CONFIG.HOST, CONFIG.PORT), RequestHandler)
    print("[INFO]Sever started on port %s." % CONFIG.PORT)
    try:
        # Open threads for sending messages and removing offline users
        threads = [RemoveOfflineUserThread()]
        for each_thread in threads:
            each_thread.start()

        server.serve_forever()

    except KeyboardInterrupt:
        server.shutdown()
        print("[INFO]Server stopped.")
